import sqlite3
import os

def init_database():
    """Initialize the database with all required tables"""
    db_path = 'data/marketplace.db'
    
    print(f"🔧 Initializing database at {db_path}")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create students table (users)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create items table (marketplace listings)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            image_path TEXT,
            seller_id INTEGER,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES students (student_id)
        )
    ''')
    
    # Create messages table (chat system)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            message_type TEXT DEFAULT 'text',
            image_attachment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES students (student_id),
            FOREIGN KEY (receiver_id) REFERENCES students (student_id)
        )
    ''')
    
    # Add any missing columns to existing tables
    try:
        cur.execute('ALTER TABLE items ADD COLUMN status TEXT DEFAULT "active"')
        print("✅ Added status column to items table")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cur.execute('ALTER TABLE items ADD COLUMN category TEXT')
        print("✅ Added category column to items table")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cur.execute('ALTER TABLE messages ADD COLUMN message_type TEXT DEFAULT "text"')
        print("✅ Added message_type column to messages table")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cur.execute('ALTER TABLE messages ADD COLUMN image_attachment TEXT')
        print("✅ Added image_attachment column to messages table")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    
    # Check what tables we have now
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    
    print(f"\n📋 Database tables created:")
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cur.fetchone()[0]
        print(f"  ✅ {table[0]} ({count} rows)")
    
    conn.close()
    print(f"\n🎉 Database initialization complete!")

if __name__ == "__main__":
    init_database()