import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

def test_login(email, password):
    try:
        conn = sqlite3.connect('data/marketplace.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("SELECT student_id, name, password FROM students WHERE email=?", (email,))
        user = cur.fetchone()
        
        if user:
            print(f"User found: {user['name']} (ID: {user['student_id']})")
            if check_password_hash(user['password'], password):
                print("✅ Password is CORRECT!")
                return True
            else:
                print("❌ Password is WRONG!")
                return False
        else:
            print("❌ User not found!")
            return False
            
        conn.close()
    except Exception as e:
        print(f'Error: {e}')
        return False

def reset_admin_password(new_password):
    try:
        conn = sqlite3.connect('data/marketplace.db')
        cur = conn.cursor()
        
        # Hash the new password
        hashed = generate_password_hash(new_password)
        
        # Update admin password
        cur.execute("UPDATE students SET password = ? WHERE email = 'admin@sea.com'", (hashed,))
        conn.commit()
        conn.close()
        
        print(f"✅ Admin password reset to: {new_password}")
        return True
    except Exception as e:
        print(f'Error resetting password: {e}')
        return False

if __name__ == "__main__":
    print("=== LOGIN DEBUGGER ===")
    
    # Test known accounts
    test_accounts = [
        ('admin@sea.com', 'admin123'),
        ('john@student.com', 'password123'),
        ('sarah@student.com', 'password123'),
        ('mike@student.com', 'password123'),
        ('emma@student.com', 'password123'),
        ('alex@student.com', 'password123')
    ]
    
    print("Testing all known accounts:")
    print("=" * 50)
    
    for email, password in test_accounts:
        print(f"\n📧 Testing: {email}")
        if test_login(email, password):
            print(f"✅ Login successful!")
        else:
            print(f"❌ Login failed!")