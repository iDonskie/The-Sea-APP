#!/usr/bin/env python
"""
Database initialization script for deployment
Ensures all necessary tables and columns exist
"""
import sqlite3
import os

def init_production_db():
    """Initialize database with all required tables and columns"""
    db_path = os.path.join(os.path.dirname(__file__), 'marketplace.db')
    
    print("🔧 Initializing database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        org TEXT,
        is_admin INTEGER DEFAULT 0,
        email_verified INTEGER DEFAULT 0,
        verification_code TEXT DEFAULT NULL,
        verification_code_expires DATETIME DEFAULT NULL
    )
    ''')
    
    # Create items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        image TEXT,
        category TEXT,
        moderation_status TEXT DEFAULT 'approved',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
    ''')
    
    # Create messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_read INTEGER DEFAULT 0,
        image_attachment TEXT,
        message_type TEXT DEFAULT 'text',
        edited_at DATETIME DEFAULT NULL,
        deleted INTEGER DEFAULT 0,
        FOREIGN KEY (sender_id) REFERENCES students(student_id),
        FOREIGN KEY (receiver_id) REFERENCES students(student_id)
    )
    ''')
    
    # Create admin_actions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER NOT NULL,
        action_type TEXT NOT NULL,
        target_type TEXT NOT NULL,
        target_id INTEGER NOT NULL,
        details TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (admin_id) REFERENCES students(student_id)
    )
    ''')
    
    conn.commit()
    
    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"✅ Database initialized successfully!")
    print(f"📊 Tables created: {', '.join(tables)}")
    
    conn.close()

if __name__ == "__main__":
    init_production_db()
