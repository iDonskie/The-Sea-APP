from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'theseaapp@gmail.com')

print(f"SendGrid API Key found: {bool(SENDGRID_API_KEY)}")
print(f"Sender Email: {SENDER_EMAIL}")

if not SENDGRID_API_KEY:
    print("❌ SendGrid API key not found in .env file!")
    exit(1)

# Test sending email
try:
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails='coco.mococoe@gmail.com',
        subject='Test Email - SEA Marketplace',
        html_content='<h1>Test Email</h1><p>If you receive this, SendGrid is working!</p><p>Your verification code is: <strong>631196</strong></p>'
    )
    
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    
    print(f"✅ Email sent successfully!")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.body}")
    print(f"Response Headers: {response.headers}")
    
except Exception as e:
    print(f"❌ Error sending email: {str(e)}")
