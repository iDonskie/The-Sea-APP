#!/usr/bin/env python3
"""
Add missing columns to messages table
"""
import sqlite3
import os
import time

def add_missing_columns():
    db_path = os.path.join('database', 'marketplace.db')
    
    try:
        # Wait for any locks to clear
        time.sleep(2)
        
        conn = sqlite3.connect(db_path, timeout=30.0)
        cur = conn.cursor()
        
        print("Adding missing columns...")
        
        # Add deleted column
        try:
            cur.execute('ALTER TABLE messages ADD COLUMN deleted INTEGER DEFAULT 0')
            print("✅ Added 'deleted' column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("ℹ️ 'deleted' column already exists")
            else:
                print(f"❌ Error adding 'deleted' column: {e}")
        
        # Add edited_at column
        try:
            cur.execute('ALTER TABLE messages ADD COLUMN edited_at TEXT')
            print("✅ Added 'edited_at' column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("ℹ️ 'edited_at' column already exists")
            else:
                print(f"❌ Error adding 'edited_at' column: {e}")
        
        conn.commit()
        
        # Verify columns were added
        cur.execute('PRAGMA table_info(messages)')
        columns = [col[1] for col in cur.fetchall()]
        
        print(f"\n📋 Current columns: {columns}")
        
        required = ['deleted', 'edited_at']
        missing = [col for col in required if col not in columns]
        
        if missing:
            print(f"⚠️ Still missing: {missing}")
        else:
            print("✅ All required columns present!")
        
        conn.close()
        return len(missing) == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = add_missing_columns()
    if success:
        print("\n🎉 Database ready for new chat system!")
    else:
        print("\n❌ Failed to update database")