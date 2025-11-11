# 📋 Deployment Checklist

Before deploying, make sure you've completed these steps:

## ✅ Pre-Deployment
- [ ] All features tested locally
- [ ] Database initialized (`python database/init_production_db.py`)
- [ ] Secret key generated (`python generate_secret_key.py`)
- [ ] Code pushed to GitHub
- [ ] `.gitignore` in place (don't commit database!)

## ✅ Platform Setup (Choose One)
### Render (Recommended)
- [ ] Signed up at render.com
- [ ] Created new Web Service
- [ ] Connected GitHub repo
- [ ] Set root directory: `SoftDesignProject`
- [ ] Set build command: `pip install -r requirements.txt && python database/init_production_db.py`
- [ ] Set start command: `gunicorn app:app`
- [ ] Added environment variable: `SECRET_KEY`
- [ ] Added environment variable: `FLASK_ENV=production`
- [ ] Deployed!

### PythonAnywhere
- [ ] Signed up at pythonanywhere.com
- [ ] Cloned repo or uploaded files
- [ ] Created virtual environment
- [ ] Installed requirements
- [ ] Initialized database
- [ ] Configured web app
- [ ] Set up WSGI file
- [ ] Reloaded app

## ✅ Post-Deployment
- [ ] App loads successfully
- [ ] Can register new user
- [ ] Can login
- [ ] Can create listing
- [ ] Can upload images
- [ ] Chat system works
- [ ] Created admin account
- [ ] Tested marketplace browsing

## 🔧 Troubleshooting
If something doesn't work:
1. Check deployment logs
2. Verify environment variables
3. Ensure database was initialized
4. Check file permissions
5. Review error messages

## 📱 Share Your App
Once deployed, share your URL:
- Render: `https://your-app-name.onrender.com`
- PythonAnywhere: `https://yourusername.pythonanywhere.com`
- Railway: `https://your-app.up.railway.app`

---

Need help? Check DEPLOY_INSTRUCTIONS.md for detailed steps!
