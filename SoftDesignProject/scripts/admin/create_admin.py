import sqlite3
import sys
from werkzeug.security import generate_password_hash

def create_admin_account():
    """Create the first admin account"""
    
    print("🛡️  SEA Admin Account Setup")
    print("=" * 40)
    
    # Check if any admin already exists
    conn = sqlite3.connect('marketplace.db')
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM students WHERE is_admin = 1")
    admin_count = cur.fetchone()[0]
    
    if admin_count > 0:
        print(f"ℹ️  {admin_count} admin account(s) already exist.")
        choice = input("Create another admin account? (y/N): ").lower().strip()
        if choice not in ['y', 'yes']:
            print("Setup cancelled.")
            conn.close()
            return
    
    print("\nCreate Admin Account:")
    print("-" * 20)
    
    # Get admin details
    while True:
        name = input("Admin Name: ").strip()
        if name:
            break
        print("❌ Name cannot be empty")
    
    while True:
        email = input("Admin Email: ").strip().lower()
        if email and '@' in email:
            # Check if email already exists
            cur.execute("SELECT student_id FROM students WHERE email = ?", (email,))
            if cur.fetchone():
                print("❌ Email already registered")
                continue
            break
        print("❌ Please enter a valid email")
    
    while True:
        password = input("Admin Password (min 6 chars): ").strip()
        if len(password) >= 6:
            break
        print("❌ Password must be at least 6 characters")
    
    # Create admin account
    try:
        password_hash = generate_password_hash(password)
        
        cur.execute("""
            INSERT INTO students (name, email, password, is_admin) 
            VALUES (?, ?, ?, 1)
        """, (name, email, password_hash))
        
        conn.commit()
        admin_id = cur.lastrowid
        
        # Log the admin creation
        cur.execute("""
            INSERT INTO admin_actions (admin_id, action_type, target_type, target_id, details)
            VALUES (?, 'create', 'admin', ?, 'Admin account created during setup')
        """, (admin_id, admin_id))
        
        conn.commit()
        
        print("\n✅ Admin account created successfully!")
        print(f"📧 Email: {email}")
        print(f"🆔 Admin ID: {admin_id}")
        print("\n🚀 You can now log in with admin privileges!")
        print("\nAdmin Features:")
        print("• Moderate all listings (approve/reject/suspend/delete)")
        print("• Manage users and promote other admins")
        print("• View activity logs")
        print("• Access admin dashboard at /admin")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creating admin account: {e}")
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    try:
        success = create_admin_account()
        if success:
            print("\n🎉 Setup complete! Start the app and log in as admin.")
        else:
            print("\n💥 Setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)