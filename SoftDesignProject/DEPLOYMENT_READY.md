# ✅ Pre-Deployment Checklist

Before deploying to Render, make sure:

## Files Ready
- [x] `requirements.txt` exists with all dependencies
- [x] `render.yaml` configuration file created
- [x] `.env.example` exists (template for environment variables)
- [x] Database initialization script ready
- [x] Admin setup script ready

## Security Check
- [ ] `.env` file is in `.gitignore` (not pushed to GitHub)
- [ ] Secret keys are environment variables
- [ ] No hardcoded passwords in code
- [ ] CSRF protection enabled
- [ ] SQL injection protection (parameterized queries)

## Code Ready
- [ ] App runs locally without errors
- [ ] Database migrations completed
- [ ] All features tested
- [ ] Email system tested
- [ ] Admin account can be created

## GitHub
- [ ] Code committed to Git
- [ ] Pushed to GitHub repository
- [ ] Repository is accessible

## Render Account
- [ ] Signed up at render.com
- [ ] GitHub connected to Render
- [ ] Payment method added (even for free tier)

## Environment Variables Ready
- [ ] `SECRET_KEY` generated
- [ ] `MAIL_USERNAME` (theseaapp@gmail.com)
- [ ] `MAIL_PASSWORD` (your app password)
- [ ] `FLASK_ENV` set to production

## Post-Deployment
- [ ] Run `init_production_db.py` in Render shell
- [ ] Create admin account with `set_admin_now.py`
- [ ] Test registration with email verification
- [ ] Test login
- [ ] Test marketplace
- [ ] Test messaging
- [ ] Test admin panel

---

## Quick Commands

### Push to GitHub
```powershell
cd "c:\Users\almar\Desktop\Codings\NEW\SoftDesignProject"
git add .
git commit -m "Ready for Render deployment"
git push origin master
```

### After Deployment - Initialize Database
```bash
# In Render Shell
cd SoftDesignProject
python database/init_production_db.py
```

### Create Admin Account
```bash
# In Render Shell
python set_admin_now.py
```

---

🚀 Ready to deploy!
