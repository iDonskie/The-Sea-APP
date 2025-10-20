import sqlite3
from werkzeug.security import generate_password_hash

def create_admin_now():
    """Create admin account right now"""
    
    try:
        conn = sqlite3.connect('marketplace.db')
        cur = conn.cursor()
        
        # Check if admin already exists
        cur.execute("SELECT * FROM students WHERE email = 'admin@sea.com'")
        existing = cur.fetchone()
        
        if existing:
            print("✅ Admin account already exists!")
            print(f"📧 Email: admin@sea.com")
            print(f"🆔 User ID: {existing[0]}")
            print(f"👤 Name: {existing[1]}")
            print(f"�️ Full record: {existing}")
            # Check if is_admin column exists and get its value
            if len(existing) > 5:  # has is_admin column
                print(f"�🛡️ Is Admin: {'Yes' if existing[5] else 'No'}")
            else:
                print("❌ is_admin column missing from this record")
        else:
            # Create admin account
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
            
            print("✅ Admin account created successfully!")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print(f"🆔 Admin ID: {admin_id}")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_admin_now()