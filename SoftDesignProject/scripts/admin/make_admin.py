import sqlite3

def make_admin():
    """Make the admin@sea.com account an actual admin"""
    
    conn = sqlite3.connect('marketplace.db')
    cur = conn.cursor()
    
    try:
        # Update the admin@sea.com account to have admin privileges
        cur.execute("UPDATE students SET is_admin = 1 WHERE email = 'admin@sea.com'")
        
        if cur.rowcount > 0:
            conn.commit()
            print("✅ admin@sea.com account promoted to admin!")
            
            # Verify the update
            cur.execute("SELECT student_id, name, email, is_admin FROM students WHERE email = 'admin@sea.com'")
            admin = cur.fetchone()
            
            if admin:
                print(f"🆔 ID: {admin[0]}")
                print(f"👤 Name: {admin[1]}")  
                print(f"📧 Email: {admin[2]}")
                print(f"🛡️ Is Admin: {'Yes' if admin[3] else 'No'}")
            
            return True
        else:
            print("❌ Admin account not found")
            return False
            
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    make_admin()