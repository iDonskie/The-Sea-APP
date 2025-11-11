# 🚀 Deploy to Render - Quick Guide

## Prerequisites
✅ GitHub account
✅ Render account (sign up at https://render.com - it's free!)
✅ Your code pushed to GitHub

## Step 1: Push Your Code to GitHub

```powershell
# In your project directory
cd "c:\Users\almar\Desktop\Codings\NEW\SoftDesignProject"

# Check git status
git status

# Add all changes
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Push to GitHub
git push origin master
```

## Step 2: Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New +" button → "Web Service"
   - Connect your GitHub repository: `fishbones-09/softdestypeshit`
   - Click "Connect"

3. **Configure Your Service**
   - **Name**: `sea-marketplace` (or whatever you want)
   - **Region**: Choose closest to your users
   - **Branch**: `master`
   - **Root Directory**: `SoftDesignProject`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

4. **Set Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   
   ```
   SECRET_KEY = <generate a random key or use existing>
   FLASK_ENV = production
   MAIL_USERNAME = theseaapp@gmail.com
   MAIL_PASSWORD = xgciykpavjzkelsc
   ```

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 3-5 minutes for build & deploy
   - Your app will be live at: `https://sea-marketplace-xxxx.onrender.com`

## Step 3: Initialize Production Database

After first deployment:

1. Go to your Render dashboard → Your service → "Shell" tab
2. Run these commands:
   ```bash
   cd SoftDesignProject
   python database/init_production_db.py
   ```

## Step 4: Set Up Your Admin Account

In the Render Shell:
```bash
python set_admin_now.py
# Follow the prompts to create your admin account
```

## Important Notes

⚠️ **Free Tier Limitations:**
- App sleeps after 15 minutes of inactivity
- Takes 30-60 seconds to wake up on first request
- 750 hours/month free (enough for a small project)

📁 **Database:**
- SQLite file persists on Render's disk
- Backup your database regularly
- For production, consider upgrading to PostgreSQL

🔒 **Security:**
- Never commit `.env` file to GitHub
- Set environment variables in Render dashboard
- Keep your `MAIL_PASSWORD` secret

## Updating Your App

Every time you make changes:
```powershell
git add .
git commit -m "Your update message"
git push origin master
```
Render will automatically redeploy! ✨

## Custom Domain (Optional)

1. In Render dashboard → Settings → "Custom Domain"
2. Add your domain (e.g., `marketplace.yourdomain.com`)
3. Update DNS records as instructed
4. Free SSL certificate automatically provided!

## Troubleshooting

**Build Failed?**
- Check build logs in Render dashboard
- Verify requirements.txt has all dependencies
- Ensure Python version compatibility

**App Not Starting?**
- Check application logs
- Verify environment variables are set
- Make sure gunicorn is in requirements.txt

**Database Issues?**
- Check if init_production_db.py was run
- Verify database file has write permissions
- Check application logs for SQL errors

## Need Help?

- Render Docs: https://render.com/docs
- Your deployment guide: `DEPLOY_INSTRUCTIONS.md`
- Check app logs in Render dashboard

---

🎉 **That's it! Your marketplace is now live!**
