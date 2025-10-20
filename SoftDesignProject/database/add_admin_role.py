import sqlite3
import sys
import os

def add_admin_role_column():
    """Add is_admin column to students table and create admin accounts table"""
    
    conn = sqlite3.connect('marketplace.db')
    cur = conn.cursor()
    
    try:
        # Check if is_admin column exists
        cur.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cur.fetchall()]
        
        if 'is_admin' not in columns:
            print("Adding is_admin column to students table...")
            cur.execute("ALTER TABLE students ADD COLUMN is_admin INTEGER DEFAULT 0")
            print("✅ is_admin column added successfully!")
        else:
            print("ℹ️  is_admin column already exists")
        
        # Create admin_actions table for logging admin activities
        cur.execute('''
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
        ''')
        print("✅ admin_actions table created/verified!")
        
        # Add status column to items if it doesn't exist (for moderation)
        cur.execute("PRAGMA table_info(items)")
        item_columns = [column[1] for column in cur.fetchall()]
        
        if 'moderation_status' not in item_columns:
            print("Adding moderation_status column to items table...")
            cur.execute("ALTER TABLE items ADD COLUMN moderation_status TEXT DEFAULT 'pending'")
            # Update existing items to 'approved' status
            cur.execute("UPDATE items SET moderation_status = 'approved' WHERE moderation_status IS NULL")
            print("✅ moderation_status column added successfully!")
        else:
            print("ℹ️  moderation_status column already exists")
            
        conn.commit()
        print("✅ Database migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error during migration: {e}")
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    success = add_admin_role_column()
    if success:
        print("\n🎉 Admin system database setup complete!")
        print("\nNext steps:")
        print("1. Run this script: python database/add_admin_role.py")
        print("2. Create admin account through the app")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)