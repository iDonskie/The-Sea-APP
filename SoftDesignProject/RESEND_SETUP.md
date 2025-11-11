# Resend Email Setup Guide

## What is Resend?
Resend is a modern email API that works reliably with hosting platforms like Render. It's much better than Gmail SMTP for production apps.

## Setup Steps

### 1. Create Resend Account
1. Go to https://resend.com/signup
2. Sign up with your email (can use Gmail)
3. Verify your email

### 2. Get API Key
1. Go to https://resend.com/api-keys
2. Click "Create API Key"
3. Give it a name like "SEA Marketplace"
4. Copy the API key (starts with `re_`)
   - **IMPORTANT**: Save this somewhere safe - you can't see it again!

### 3. Update Render Environment Variables
1. Go to your Render dashboard
2. Select your service (The SEA App)
3. Click "Environment" in the left sidebar
4. **Remove old variables:**
   - Delete `MAIL_USERNAME`
   - Delete `MAIL_PASSWORD`
   - Delete `MAIL_SERVER`
   - Delete `MAIL_PORT`
   - Delete `MAIL_USE_TLS`
   
5. **Add new variables:**
   - Key: `RESEND_API_KEY`
   - Value: `re_your_actual_api_key_here` (paste your API key)
   
   - Key: `SENDER_EMAIL`
   - Value: `onboarding@resend.dev` (for testing)

6. Click "Save Changes"
7. Service will automatically redeploy

### 4. Test It!
1. Wait 1-2 minutes for Render to redeploy
2. Go to your app and register with a new email
3. You should receive the verification code within seconds!

## Email Addresses

### For Testing (Free)
- **Sender**: `onboarding@resend.dev`
- This works immediately, no setup needed
- Can send to any email address
- Good for development and testing

### For Production (Your Own Domain)
Once you're ready for production:
1. Add and verify your domain in Resend
2. Update `SENDER_EMAIL` to `noreply@yourdomain.com`
3. This makes emails look more professional

## Free Tier Limits
- ✅ 100 emails per day
- ✅ 3,000 emails per month
- ✅ All features included
- More than enough for a student marketplace!

## Troubleshooting

### Still not receiving emails?
1. Check spam/junk folder
2. Verify API key is correct in Render environment variables
3. Check Render logs for errors
4. Make sure `RESEND_API_KEY` is set (not `MAIL_PASSWORD`)

### API Key not working?
- Make sure you copied the entire key
- Keys start with `re_`
- No spaces before or after

### Want to check if it's working?
1. Go to https://resend.com/emails
2. You'll see a log of all sent emails
3. Check delivery status

## Need Help?
- Resend docs: https://resend.com/docs
- Resend support: Very responsive via their dashboard
