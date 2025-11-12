# PostgreSQL Migration Guide

## Why PostgreSQL?
- ✅ **Persistent storage** - Data never disappears
- ✅ **Free tier on Render** - No cost
- ✅ **Better performance** - Handles concurrent users better
- ✅ **Production ready** - What real apps use

## Setup Steps

### 1. Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `sea-marketplace-db`
   - **Database**: `sea_marketplace`
   - **User**: Leave default or `sea_user`
   - **Region**: Same as your web service (Singapore)
   - **Instance Type**: **Free**
4. Click **"Create Database"**
5. Wait 1-2 minutes for creation

### 2. Connect Database to Your App

1. In Render dashboard, click on your **PostgreSQL database**
2. Find **"Internal Database URL"** (starts with `postgresql://` or `postgres://`)
3. **Copy it**
4. Go to your **Web Service** → **Environment** tab
5. Add new environment variable:
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL
6. Click **Save**

### 3. Initialize the Database

After the app redeploys with `DATABASE_URL` set:

**Option A: Using the web interface**
Visit: `https://your-app.onrender.com/init-db`

**Option B: Using Render Shell (if you have paid plan)**
```bash
python init_postgres.py
```

This creates all the necessary tables in PostgreSQL.

### 4. Done!

Your app now uses PostgreSQL! Data will persist forever, even when the app sleeps.

## Migration Notes

### What Changed
- **Development (local)**: Still uses SQLite (`database/marketplace.db`)
- **Production (Render)**: Now uses PostgreSQL
- Code automatically detects which database to use based on `DATABASE_URL` environment variable

### SQL Differences Handled
The app code now handles differences between SQLite and PostgreSQL:
- **AUTOINCREMENT** → **SERIAL**
- **INTEGER PRIMARY KEY** → **SERIAL PRIMARY KEY**
- **CURRENT_TIMESTAMP** works in both

### Testing Locally
Your local development still uses SQLite, so you can test without PostgreSQL installed.

## Troubleshooting

### "relation does not exist" error
- You need to initialize the database
- Visit `/init-db` or run `init_postgres.py`

### App won't start after adding DATABASE_URL
- Check the URL is correct
- Make sure `psycopg2-binary` is in requirements.txt
- Check deployment logs for specific errors

### Need to reset the database
1. Go to Render → Your PostgreSQL database
2. Click **"Delete Database"** (be careful!)
3. Create a new one
4. Update `DATABASE_URL` in your web service
5. Initialize again with `/init-db`

### Want to migrate existing data
If you have important data in the old SQLite database:
1. Save it locally before deploying
2. After PostgreSQL is set up, manually re-create the data
3. Or use a migration script (more complex)

## Free Tier Limits

PostgreSQL Free Tier on Render:
- ✅ 256 MB storage
- ✅ 90 days, then expires (but you can create a new one)
- ✅ Perfect for small to medium apps
- ✅ Plenty for a student marketplace!

## Next Steps

After migration:
1. Register new accounts
2. Create listings
3. Test that data persists after app sleeps
4. Your marketplace is now production-ready! 🎉
