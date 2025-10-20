import sqlite3
import shutil
import os

def fix_database_in_correct_location():
    """Fix the database that the Flask app actually uses"""
    
    db_path = os.path.join('database', 'marketplace.db')
    print(f"🔧 Fixing database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        print("🔍 Checking current schema...")
        
        # Check and add is_admin column to students table
        cur.execute("PRAGMA table_info(students)")
        students_columns = [col[1] for col in cur.fetchall()]
        print(f"📋 Students columns: {students_columns}")
        
        if 'is_admin' not in students_columns:
            print("➕ Adding is_admin column to students table...")
            cur.execute("ALTER TABLE students ADD COLUMN is_admin INTEGER DEFAULT 0")
            print("✅ is_admin column added!")
        else:
            print("ℹ️  is_admin column already exists")
        
        # Check and add moderation_status column to items table
        cur.execute("PRAGMA table_info(items)")
        items_columns = [col[1] for col in cur.fetchall()]
        print(f"📦 Items columns: {items_columns}")
        
        if 'moderation_status' not in items_columns:
            print("➕ Adding moderation_status column to items table...")
            cur.execute("ALTER TABLE items ADD COLUMN moderation_status TEXT DEFAULT 'approved'")
            # Set all existing items to approved so they remain visible
            cur.execute("UPDATE items SET moderation_status = 'approved' WHERE moderation_status IS NULL")
            print("✅ moderation_status column added and existing items set to approved!")
        else:
            print("ℹ️  moderation_status column already exists")
        
        # Create admin_actions table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_actions (
            action_id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            target_type TEXT NOT NULL,
            target_id INTEGER NOT NULL,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES students(student_id)
        )
        """)
        print("✅ admin_actions table created/verified!")
        
        # Create admin user if doesn't exist
        cur.execute("SELECT * FROM students WHERE email = 'admin@sea.com'")
        admin = cur.fetchone()
        
        if not admin:
            print("➕ Creating admin user...")
            from werkzeug.security import generate_password_hash
            
            password_hash = generate_password_hash('admin123')
            cur.execute("""
                INSERT INTO students (name, email, password, is_admin) 
                VALUES (?, ?, ?, 1)
            """, ('Admin', 'admin@sea.com', password_hash))
            
            admin_id = cur.lastrowid
            print(f"✅ Admin user created with ID: {admin_id}")
        else:
            # Make sure existing admin has admin privileges
            cur.execute("UPDATE students SET is_admin = 1 WHERE email = 'admin@sea.com'")
            print("✅ Admin privileges updated for existing user")
        
        conn.commit()
        print("\n🎉 Database schema updated successfully!")
        
        # Final verification
        print("\n🔍 Final verification...")
        
        cur.execute("PRAGMA table_info(students)")
        students_columns = [col[1] for col in cur.fetchall()]
        print(f"📋 Final Students columns: {students_columns}")
        
        cur.execute("PRAGMA table_info(items)")
        items_columns = [col[1] for col in cur.fetchall()]
        print(f"📦 Final Items columns: {items_columns}")
        
        cur.execute("SELECT student_id, name, email, is_admin FROM students WHERE email = 'admin@sea.com'")
        admin = cur.fetchone()
        if admin:
            print(f"🛡️  Admin user: ID={admin[0]}, Name={admin[1]}, Email={admin[2]}, IsAdmin={admin[3]}")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = fix_database_in_correct_location()
    if success:
        print("\n🎊 Database is now ready for the Flask app!")
        print("\n📍 Login credentials:")
        print("   📧 Email: admin@sea.com")
        print("   🔑 Password: admin123")
    else:
        print("\n💥 Database fix failed!")