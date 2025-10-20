import sqlite3
import os

def migrate_multiple_images():
    """
    Migrate the database to support multiple images per item.
    Creates a new item_images table and migrates existing image data.
    """
    # Get the database path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'marketplace.db')
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create the new item_images table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS item_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            image_filename TEXT NOT NULL,
            is_primary INTEGER DEFAULT 0,
            upload_order INTEGER DEFAULT 0,
            FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE
        )
    ''')
    
    # Migrate existing images from items table to item_images table
    cur.execute("SELECT item_id, image FROM items WHERE image IS NOT NULL AND image != ''")
    existing_images = cur.fetchall()
    
    for item_id, image_filename in existing_images:
        # Insert the existing image as the primary image
        cur.execute('''
            INSERT INTO item_images (item_id, image_filename, is_primary, upload_order)
            VALUES (?, ?, 1, 1)
        ''', (item_id, image_filename))
    
    conn.commit()
    conn.close()
    print(f"Migration completed. Migrated {len(existing_images)} existing images.")
    print("New item_images table created successfully.")

if __name__ == "__main__":
    migrate_multiple_images()