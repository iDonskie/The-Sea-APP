#!/usr/bin/env python3
"""
Approve all pending items in the database
"""
import sqlite3
import os

def approve_pending_items():
    """Approve all items with pending moderation status"""
    db_path = os.path.join('database', 'marketplace.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Check how many pending items we have
        cur.execute("SELECT COUNT(*) as count FROM items WHERE moderation_status = 'pending'")
        pending_count = cur.fetchone()[0]
        
        if pending_count == 0:
            print("✅ No pending items found. All items are already approved!")
            return True
        
        # Show pending items
        print(f"📋 Found {pending_count} pending item(s):")
        cur.execute("SELECT item_id, item_name, student_id FROM items WHERE moderation_status = 'pending'")
        pending_items = cur.fetchall()
        
        for item in pending_items:
            print(f"   ID {item[0]}: '{item[1]}' (User {item[2]})")
        
        # Approve all pending items
        cur.execute("UPDATE items SET moderation_status = 'approved' WHERE moderation_status = 'pending'")
        approved_count = cur.rowcount
        
        conn.commit()
        
        print(f"\n✅ Successfully approved {approved_count} item(s)!")
        
        # Show final status
        cur.execute("SELECT moderation_status, COUNT(*) as count FROM items GROUP BY moderation_status")
        status_counts = cur.fetchall()
        
        print("\n📊 Current item status:")
        for status in status_counts:
            print(f"   {status[0]}: {status[1]} items")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Approving all pending items...")
    print("=" * 40)
    
    success = approve_pending_items()
    
    if success:
        print("\n🎉 All done! Your items should now appear in the marketplace!")
        print("🌐 Check: http://localhost:5000/marketplace")
    else:
        print("\n❌ Failed to approve items")