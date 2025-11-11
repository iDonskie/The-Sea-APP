from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

print("=" * 60)
print("📧 EMAIL TEST")
print("=" * 60)
print(f"Mail Server: {app.config['MAIL_SERVER']}")
print(f"Mail Port: {app.config['MAIL_PORT']}")
print(f"Mail Username: {app.config['MAIL_USERNAME']}")
print(f"Mail Password: {'***' + app.config['MAIL_PASSWORD'][-4:] if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
print("=" * 60)

try:
    with app.app_context():
        msg = Message(
            subject="Test Email - SEA Marketplace",
            recipients=['almark.occeno@gmail.com']
        )
        msg.body = "This is a test email. If you received this, email configuration is working!"
        msg.html = "<h1>✅ Email Works!</h1><p>Your email configuration is set up correctly.</p>"
        
        print("\n📤 Sending test email...")
        mail.send(msg)
        print("✅ Email sent successfully!")
        print("\nCheck your inbox (and spam folder) for the test email.")
        
except Exception as e:
    print(f"\n❌ Error sending email: {e}")
    print("\nCommon fixes:")
    print("1. Make sure you're using Gmail App Password (not regular password)")
    print("2. Enable 2-Step Verification in Google Account")
    print("3. Check if .env file has correct MAIL_USERNAME and MAIL_PASSWORD")
