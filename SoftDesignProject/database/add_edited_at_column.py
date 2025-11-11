"""
Migration script to add edited_at column to messages table
This column tracks when a message was last edited
"""
import sqlite3
import os

def add_edited_at_column():
    # Get database path
    db_path = os.path.join(os.path.dirname(__file__), 'marketplace.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(messages)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'edited_at' in columns:
            print("✅ Column 'edited_at' already exists in messages table")
            conn.close()
            return
        
        # Add the edited_at column
        print("Adding 'edited_at' column to messages table...")
        cursor.execute("""
            ALTER TABLE messages 
            ADD COLUMN edited_at DATETIME DEFAULT NULL
        """)
        
        conn.commit()
        print("✅ Successfully added 'edited_at' column to messages table")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(messages)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nCurrent messages table columns: {', '.join(columns)}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_edited_at_column()
