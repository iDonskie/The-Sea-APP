import sqlite3
from werkzeug.security import check_password_hash

def debug_login():
    """Debug the exact login process"""
    
    conn = sqlite3.connect('marketplace.db')
    cur = conn.cursor()
    
    try:
        # Test the exact login process
        email = "admin@sea.com"
        password = "admin123"
        
        print(f"🔍 Testing login with:")
        print(f"📧 Email: '{email}'")
        print(f"🔑 Password: '{password}'")
        
        # Check all accounts with similar email
        cur.execute("SELECT student_id, name, email, password, is_admin FROM students WHERE email LIKE '%admin%'")
        accounts = cur.fetchall()
        
        print(f"\n📋 Found {len(accounts)} admin-related accounts:")
        
        for i, account in enumerate(accounts, 1):
            print(f"\n{i}. Account:")
            print(f"   🆔 ID: {account[0]}")
            print(f"   👤 Name: {account[1]}")
            print(f"   📧 Email: '{account[2]}'")
            print(f"   🛡️ Is Admin: {'Yes' if account[4] else 'No'}")
            
            # Test password for this account
            if check_password_hash(account[3], password):
                print(f"   ✅ Password 'admin123' WORKS for this account!")
            else:
                print(f"   ❌ Password 'admin123' doesn't work for this account")
        
        # Test the exact query the login function uses
        print(f"\n🔍 Testing exact login query...")
        cur.execute("SELECT student_id, name, password FROM students WHERE email=?", (email.lower(),))
        user = cur.fetchone()
        
        if user:
            print(f"✅ User found with email '{email.lower()}'")
            print(f"🆔 ID: {user[0]}")
            print(f"👤 Name: {user[1]}")
            
            if check_password_hash(user[2], password):
                print(f"✅ Password verification: SUCCESS")
                print(f"🎉 Login should work!")
            else:
                print(f"❌ Password verification: FAILED")
                print(f"💡 There might be a password hash issue")
        else:
            print(f"❌ No user found with email '{email.lower()}'")
            
            # Try without lowercasing
            cur.execute("SELECT student_id, name, password FROM students WHERE email=?", (email,))
            user2 = cur.fetchone()
            
            if user2:
                print(f"✅ User found with original case email '{email}'")
                if check_password_hash(user2[2], password):
                    print(f"✅ Password works with original case email!")
                else:
                    print(f"❌ Password still doesn't work")
            else:
                print(f"❌ No user found with original case either")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    debug_login()