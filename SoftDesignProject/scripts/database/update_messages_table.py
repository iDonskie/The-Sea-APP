#!/usr/bin/env python3
"""
Check and update messages table for new chat system
"""
import sqlite3
import os

def check_and_update_messages_table():
    """Check if messages table has required columns and add them if missing"""
    db_path = os.path.join('database', 'marketplace.db')
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        cur = conn.cursor()
        
        # Check current table structure
        cur.execute("PRAGMA table_info(messages)")
        columns = {col[1]: col[2] for col in cur.fetchall()}
        
        print("Current messages table columns:")
        for name, type_info in columns.items():
            print(f"  {name}: {type_info}")
        
        # Add missing columns
        missing_columns = []
        
        if 'deleted' not in columns:
            cur.execute("ALTER TABLE messages ADD COLUMN deleted INTEGER DEFAULT 0")
            missing_columns.append('deleted')
        
        if 'edited_at' not in columns:
            cur.execute("ALTER TABLE messages ADD COLUMN edited_at TEXT")
            missing_columns.append('edited_at')
        
        if 'message_type' not in columns:
            cur.execute("ALTER TABLE messages ADD COLUMN message_type TEXT DEFAULT 'text'")
            missing_columns.append('message_type')
        
        if missing_columns:
            print(f"\nAdded missing columns: {missing_columns}")
            conn.commit()
        else:
            print("\nAll required columns already exist!")
        
        # Show updated structure
        cur.execute("PRAGMA table_info(messages)")
        columns = cur.fetchall()
        
        print(f"\nUpdated messages table structure:")
        for col in columns:
            print(f"  {col[1]}: {col[2]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_and_update_messages_table()