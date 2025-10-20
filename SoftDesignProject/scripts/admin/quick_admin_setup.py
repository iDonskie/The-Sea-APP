import sqlite3
from werkzeug.security import generate_password_hash

def setup_admin():
    """Manually create admin account"""
    
    conn = sqlite3.connect('marketplace.db')
    cur = conn.cursor()
    
    # Create admin account
    name = "Admin"
    email = "admin@sea.com"
    password = "admin123"  # Change this in production!
    
    password_hash = generate_password_hash(password)
    
    try:
        cur.execute("""
            INSERT INTO students (name, email, password, is_admin) 
            VALUES (?, ?, ?, 1)
        """, (name, email, password_hash))
        
        conn.commit()
        admin_id = cur.lastrowid
        
        print(f"✅ Admin account created!")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"🆔 Admin ID: {admin_id}")
        print("\n⚠️  Remember to change the password after first login!")
        
    except sqlite3.IntegrityError:
        print("❌ Admin account already exists or email is taken")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_admin()