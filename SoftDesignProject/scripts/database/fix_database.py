import sqlite3

def fix_database_schema():
    """Add missing columns to existing database"""
    
    conn = sqlite3.connect('marketplace.db')
    cur = conn.cursor()
    
    try:
        print("🔧 Fixing database schema...")
        
        # Check and add is_admin column to students table
        cur.execute("PRAGMA table_info(students)")
        students_columns = [col[1] for col in cur.fetchall()]
        
        if 'is_admin' not in students_columns:
            print("➕ Adding is_admin column to students table...")
            cur.execute("ALTER TABLE students ADD COLUMN is_admin INTEGER DEFAULT 0")
            print("✅ is_admin column added!")
        else:
            print("ℹ️  is_admin column already exists")
        
        # Check and add moderation_status column to items table
        cur.execute("PRAGMA table_info(items)")
        items_columns = [col[1] for col in cur.fetchall()]
        
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
        
        conn.commit()
        print("\n🎉 Database schema updated successfully!")
        
        # Verify the changes
        print("\n🔍 Verifying changes...")
        
        cur.execute("PRAGMA table_info(students)")
        students_columns = [col[1] for col in cur.fetchall()]
        print(f"📋 Students columns: {students_columns}")
        
        cur.execute("PRAGMA table_info(items)")  
        items_columns = [col[1] for col in cur.fetchall()]
        print(f"📦 Items columns: {items_columns}")
        
        if 'is_admin' in students_columns and 'moderation_status' in items_columns:
            print("\n✅ All required columns are present!")
            return True
        else:
            print("\n❌ Some columns are still missing!")
            return False
            
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database_schema()