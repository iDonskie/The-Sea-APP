import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def fix_admin_password():
    """Fix the admin account password"""
    
    conn = sqlite3.connect('marketplace.db')
    cur = conn.cursor()
    
    try:
        # Check current admin account
        cur.execute("SELECT student_id, name, email, password, is_admin FROM students WHERE email = 'admin@sea.com'")
        admin = cur.fetchone()
        
        if admin:
            print("🔍 Current admin account:")
            print(f"🆔 ID: {admin[0]}")
            print(f"👤 Name: {admin[1]}")
            print(f"📧 Email: {admin[2]}")
            print(f"🛡️ Is Admin: {'Yes' if admin[4] else 'No'}")
            
            # Test current password
            current_hash = admin[3]
            test_password = "admin123"
            
            if check_password_hash(current_hash, test_password):
                print("✅ Current password 'admin123' works!")
                return True
            else:
                print("❌ Current password 'admin123' doesn't work!")
                print("🔧 Updating password...")
                
                # Generate new password hash
                new_hash = generate_password_hash(test_password)
                
                # Update the password
                cur.execute("UPDATE students SET password = ? WHERE email = 'admin@sea.com'", (new_hash,))
                conn.commit()
                
                print("✅ Password updated successfully!")
                
                # Verify the new password
                if check_password_hash(new_hash, test_password):
                    print("✅ New password verified - 'admin123' should work now!")
                    return True
                else:
                    print("❌ Password verification failed!")
                    return False
        else:
            print("❌ Admin account not found!")
            print("🔧 Creating new admin account...")
            
            # Create new admin account
            name = "Admin"
            email = "admin@sea.com"
            password = "admin123"
            password_hash = generate_password_hash(password)
            
            cur.execute("""
                INSERT INTO students (name, email, password, is_admin) 
                VALUES (?, ?, ?, 1)
            """, (name, email, password_hash))
            
            conn.commit()
            admin_id = cur.lastrowid
            
            print("✅ New admin account created!")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print(f"🆔 Admin ID: {admin_id}")
            
            return True
            
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    fix_admin_password()