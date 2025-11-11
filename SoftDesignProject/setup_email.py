#!/usr/bin/env python
"""
Interactive setup script for email configuration
"""
import os

def setup_email_config():
    print("=" * 60)
    print("📧 EMAIL VERIFICATION SETUP")
    print("=" * 60)
    print("\nThis script will help you set up email verification.")
    print("\nFor Gmail, you need to:")
    print("1. Enable 2-Step Verification in Google Account")
    print("2. Generate an App Password (Security → App passwords)")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    input()
    
    print("\n" + "=" * 60)
    print("Enter your email configuration:")
    print("=" * 60)
    
    mail_username = input("\nEmail address (e.g., your-email@gmail.com): ").strip()
    mail_password = input("App password (16-digit from Google): ").strip().replace(" ", "")
    
    # Create .env file content
    env_content = f"""# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME={mail_username}
MAIL_PASSWORD={mail_password}
MAIL_DEFAULT_SENDER={mail_username}

# Security
SECRET_KEY={os.urandom(24).hex()}
FLASK_ENV=development
"""
    
    # Ask if user wants to save to .env file
    print("\n" + "=" * 60)
    print("Configuration ready!")
    print("=" * 60)
    save = input("\nSave to .env file? (y/n): ").lower().strip()
    
    if save == 'y':
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ Configuration saved to .env file!")
        print("\n⚠️  IMPORTANT: Install python-dotenv to load .env automatically:")
        print("   pip install python-dotenv")
        print("\n   Then add to app.py (at the top):")
        print("   from dotenv import load_dotenv")
        print("   load_dotenv()")
    else:
        print("\n📋 Set these environment variables manually:")
        print("\nWindows PowerShell:")
        print(f'$env:MAIL_USERNAME="{mail_username}"')
        print(f'$env:MAIL_PASSWORD="{mail_password}"')
        
        print("\nLinux/Mac:")
        print(f'export MAIL_USERNAME="{mail_username}"')
        print(f'export MAIL_PASSWORD="{mail_password}"')
    
    print("\n" + "=" * 60)
    print("✅ Setup complete! You can now test email verification.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        setup_email_config()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
