# ✅ Email Verification - Quick Start Guide

## What Was Added?

Your app now requires **email verification** for new user registrations! Users receive a 6-digit code via email that they must enter to activate their account.

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Gmail App Password

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already enabled)
3. Go to https://myaccount.google.com/apppasswords
4. Generate password for "Mail"
5. **Copy the 16-digit password** (like: `abcd efgh ijkl mnop`)

### Step 2: Configure Email

**Option A - Run Setup Script (Easiest):**
```bash
cd SoftDesignProject
python setup_email.py
```

**Option B - Manual Setup:**
Create `.env` file in `SoftDesignProject` folder:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your16digitapppassword
```

### Step 3: Test It!

```bash
python run.py
```

1. Register a new account at http://localhost:5000/register
2. Check your email for the 6-digit code
3. Enter the code on the verification page
4. Done! You can now log in

## ✅ For Existing Users

Verify all existing users in your database:
```bash
python -c "import sqlite3; conn = sqlite3.connect('database/marketplace.db'); conn.execute('UPDATE students SET email_verified = 1'); conn.commit(); print('✅ All users verified!')"
```

## 🐛 Troubleshooting

**Email not sending?**
- Use App Password, not your regular Gmail password
- Remove spaces from the 16-digit password
- Check spam/junk folder

**Need to test without email?**
- Manually verify users using the command above
- Or temporarily comment out the email check in login()

## 📁 What Was Changed?

- ✅ Database: Added `email_verified`, `verification_code`, `verification_code_expires` columns
- ✅ Registration: Now sends verification email
- ✅ Login: Blocks unverified users
- ✅ New page: `/verify-email` for code entry
- ✅ New feature: Resend verification code

## 🌐 For Production (Render/Railway)

Add environment variables:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

**Full documentation**: See `EMAIL_SETUP.md` for detailed instructions!
