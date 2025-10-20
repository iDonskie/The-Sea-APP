import sqlite3
import os

def add_category_column():
    """
    Add category column to the items table to support categorization.
    """
    # Get the database path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'marketplace.db')
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Check if category column already exists
    cur.execute("PRAGMA table_info(items)")
    columns = [row[1] for row in cur.fetchall()]
    
    if 'category' not in columns:
        # Add category column to items table with a default value
        cur.execute('ALTER TABLE items ADD COLUMN category TEXT DEFAULT "other"')
        print("Added category column to items table.")
        
        # Update existing items with appropriate categories based on item names (simple heuristics)
        cur.execute("UPDATE items SET category = 'books' WHERE LOWER(item_name) LIKE '%book%' OR LOWER(description) LIKE '%book%'")
        cur.execute("UPDATE items SET category = 'electronics' WHERE LOWER(item_name) LIKE '%phone%' OR LOWER(item_name) LIKE '%laptop%' OR LOWER(item_name) LIKE '%computer%' OR LOWER(item_name) LIKE '%electronic%'")
        cur.execute("UPDATE items SET category = 'supplies' WHERE LOWER(item_name) LIKE '%pen%' OR LOWER(item_name) LIKE '%paper%' OR LOWER(item_name) LIKE '%supplies%' OR LOWER(item_name) LIKE '%notebook%'")
        cur.execute("UPDATE items SET category = 'clothing' WHERE LOWER(item_name) LIKE '%shirt%' OR LOWER(item_name) LIKE '%clothes%' OR LOWER(item_name) LIKE '%jacket%' OR LOWER(item_name) LIKE '%dress%'")
        cur.execute("UPDATE items SET category = 'appliances' WHERE LOWER(item_name) LIKE '%appliance%' OR LOWER(item_name) LIKE '%refrigerator%' OR LOWER(item_name) LIKE '%microwave%'")
        
        print("Updated existing items with appropriate categories based on names/descriptions.")
    else:
        print("Category column already exists.")
    
    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    add_category_column()