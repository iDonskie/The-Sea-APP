import sqlite3
import os

db_path = 'SoftDesignProject/database/marketplace.db'

if not os.path.exists(db_path):
    print(f"❌ Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    # Create messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_read INTEGER DEFAULT 0,
            image_attachment TEXT,
            message_type TEXT DEFAULT 'text',
            edited_at DATETIME,
            FOREIGN KEY (sender_id) REFERENCES students(student_id),
            FOREIGN KEY (receiver_id) REFERENCES students(student_id)
        )
    """)
    print("✅ Messages table created")
    
    # Create item_images table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS item_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            image_filename TEXT NOT NULL,
            is_primary INTEGER DEFAULT 0,
            upload_order INTEGER DEFAULT 0,
            FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
        )
    """)
    print("✅ Item_images table created")
    
    # Create admin_actions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_actions (
            action_id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            action_type TEXT,
            target_type TEXT,
            target_id INTEGER,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES students(student_id)
        )
    """)
    print("✅ Admin_actions table created")
    
    # Check if items table has moderation_status column
    cur.execute("PRAGMA table_info(items)")
    columns = [row[1] for row in cur.fetchall()]
    
    if 'moderation_status' not in columns:
        cur.execute("ALTER TABLE items ADD COLUMN moderation_status TEXT DEFAULT 'approved'")
        print("✅ Added moderation_status column to items table")
    
    if 'category' not in columns:
        cur.execute("ALTER TABLE items ADD COLUMN category TEXT DEFAULT 'other'")
        print("✅ Added category column to items table")
    
    if 'contact' not in columns:
        cur.execute("ALTER TABLE items ADD COLUMN contact TEXT")
        print("✅ Added contact column to items table")
    
    if 'payment' not in columns:
        cur.execute("ALTER TABLE items ADD COLUMN payment TEXT")
        print("✅ Added payment column to items table")
    
    if 'status' not in columns:
        cur.execute("ALTER TABLE items ADD COLUMN status TEXT DEFAULT 'available'")
        print("✅ Added status column to items table")
    
    conn.commit()
    print("\n✅ All tables initialized successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
