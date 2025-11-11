# 📧 Email Verification Setup Guide

## Overview
Your app now requires email verification for new user registrations! Users will receive a 6-digit code via email to verify their account.

## Local Development Setup

### Step 1: Create Gmail App Password

1. **Go to your Google Account**: https://myaccount.google.com/
2. **Enable 2-Step Verification**:
   - Go to Security → 2-Step Verification
   - Follow the setup process
3. **Create App Password**:
   - Go to Security → App passwords (at the bottom)
   - Select "Mail" and your device
   - Google will generate a 16-character password
   - **Copy this password** (you won't see it again)

### Step 2: Configure Environment Variables

Create a `.env` file in the `SoftDesignProject` directory:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop  # Your 16-digit app password (spaces optional)
MAIL_DEFAULT_SENDER=your-email@gmail.com
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Step 3: Load Environment Variables

**Option A - Manual (Windows PowerShell):**
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
```

**Option B - Using python-dotenv:**
```bash
pip install python-dotenv
```

Then add to the top of `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Step 4: Test Email Sending

Run your app and register a new account. You should receive an email with a verification code!

---

## Production Deployment

### Render/Railway Setup

Add these environment variables in your platform's dashboard:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-digit-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
```

### Alternative Email Services

**SendGrid (Recommended for production):**
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

**Mailgun:**
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=your-mailgun-username
MAIL_PASSWORD=your-mailgun-password
```

---

## How It Works

1. **User registers** → Account created but not verified
2. **Email sent** → 6-digit code sent to user's email
3. **User enters code** → If valid, account is verified
4. **User can login** → Only verified users can access the app

### Features:
- ✅ 6-digit verification codes
- ✅ Codes expire after 15 minutes
- ✅ Resend code functionality
- ✅ Beautiful email templates (HTML + plain text)
- ✅ Blocks login until email is verified

---

## Troubleshooting

### Email not sending?
- Check if Gmail App Password is correct
- Make sure 2-Step Verification is enabled
- Check spam folder
- Verify MAIL_USERNAME and MAIL_PASSWORD are set correctly

### "Authentication failed" error?
- Use App Password, not your regular Gmail password
- Remove spaces from the 16-digit password
- Make sure Less Secure Apps is NOT needed (App Passwords bypass this)

### Testing without email?
For development, you can manually verify users in the database:
```bash
python -c "import sqlite3; conn = sqlite3.connect('database/marketplace.db'); conn.execute('UPDATE students SET email_verified = 1 WHERE email = \"your@email.com\"'); conn.commit(); print('User verified!')"
```

---

## Security Notes

- Never commit `.env` file to git (already in `.gitignore`)
- Use App Passwords, not regular passwords
- Rotate secrets regularly
- Use different passwords for dev and production
- Consider using SendGrid/Mailgun for production (better deliverability)

---

Need help? Check the console logs for detailed error messages!
