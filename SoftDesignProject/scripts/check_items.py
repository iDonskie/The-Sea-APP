#!/usr/bin/env python3
"""
Check all items in the database
"""
import sqlite3
import os

def check_all_items():
    """Check all items and their status"""
    db_path = os.path.join('database', 'marketplace.db')
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Get all items
        cur.execute("SELECT item_id, item_name, moderation_status, student_id, category FROM items ORDER BY item_id DESC")
        items = cur.fetchall()
        
        if not items:
            print("📭 No items found in database")
            return
        
        print(f"📋 Found {len(items)} item(s) in database:")
        for item in items:
            print(f"   ID {item[0]}: '{item[1]}' - Status: {item[2]} (User {item[3]}, Category: {item[4]})")
        
        # Check status breakdown
        cur.execute("SELECT moderation_status, COUNT(*) as count FROM items GROUP BY moderation_status")
        status_counts = cur.fetchall()
        
        print(f"\n📊 Status breakdown:")
        for status in status_counts:
            print(f"   {status[0]}: {status[1]} items")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_all_items()