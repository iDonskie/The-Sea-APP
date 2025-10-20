import sqlite3
from werkzeug.security import check_password_hash

def test_admin_login():
    """Test if admin credentials work"""
    
    try:
        conn = sqlite3.connect('marketplace.db')
        cur = conn.cursor()
        
        # Get admin user
        cur.execute("SELECT student_id, name, email, password, is_admin FROM students WHERE email = 'admin@sea.com'")
        user = cur.fetchone()
        
        if not user:
            print("❌ Admin user not found!")
            return False
            
        print("✅ Admin user found:")
        print(f"🆔 ID: {user[0]}")
        print(f"👤 Name: {user[1]}")
        print(f"📧 Email: {user[2]}")
        print(f"🛡️ Is Admin: {'Yes' if user[4] else 'No'}")
        
        # Test password
        password = "admin123"
        password_hash = user[3]
        
        if check_password_hash(password_hash, password):
            print("✅ Password verification: SUCCESS")
            print("🎉 Admin login should work!")
        else:
            print("❌ Password verification: FAILED")
            print("💥 There's an issue with the password hash")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_admin_login()