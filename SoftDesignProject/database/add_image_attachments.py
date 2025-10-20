import sqlite3
import os

def add_image_attachment_support():
    """
    Add image attachment support to the messages table.
    """
    # Get the database path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'marketplace.db')
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Check if image_attachment column already exists
    cur.execute("PRAGMA table_info(messages)")
    columns = [row[1] for row in cur.fetchall()]
    
    if 'image_attachment' not in columns:
        # Add image_attachment column to messages table
        cur.execute('ALTER TABLE messages ADD COLUMN image_attachment TEXT')
        print("Added image_attachment column to messages table.")
    else:
        print("image_attachment column already exists.")
    
    # Also add message_type column to distinguish between text and image messages
    if 'message_type' not in columns:
        cur.execute('ALTER TABLE messages ADD COLUMN message_type TEXT DEFAULT "text"')
        print("Added message_type column to messages table.")
    else:
        print("message_type column already exists.")
    
    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    add_image_attachment_support()