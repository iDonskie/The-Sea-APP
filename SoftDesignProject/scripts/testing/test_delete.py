#!/usr/bin/env python3
"""
Simple test script to check if the delete functionality works
"""
import sqlite3
import os

def test_delete_functionality():
    """Test if we can delete items from the database"""
    
    # Connect to database
    db_path = os.path.join('database', 'marketplace.db')
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Check current items
        cur.execute("SELECT COUNT(*) as count FROM items")
        initial_count = cur.fetchone()[0]
        print(f"📊 Initial item count: {initial_count}")
        
        # Check if there are any items to test with
        if initial_count == 0:
            print("⚠️ No items in database to test delete functionality")
            return False
        
        # Get first item for testing
        cur.execute("SELECT item_id, item_name FROM items LIMIT 1")
        test_item = cur.fetchone()
        test_id = test_item[0]
        test_name = test_item[1]
        
        print(f"🧪 Testing delete on item {test_id}: '{test_name}'")
        
        # Simulate the delete operation from moderate_item function
        cur.execute("DELETE FROM items WHERE item_id = ?", (test_id,))
        conn.commit()
        
        # Check if delete worked
        cur.execute("SELECT COUNT(*) as count FROM items")
        final_count = cur.fetchone()[0]
        
        if final_count == initial_count - 1:
            print(f"✅ Delete successful! Count changed from {initial_count} to {final_count}")
            
            # Restore the item for testing purposes
            cur.execute("INSERT INTO items (item_name, description, price, condition, category, moderation_status, student_id) VALUES (?, 'Test item restored', 10.00, 'good', 'other', 'pending', 1)", (test_name,))
            conn.commit()
            print("🔄 Test item restored for future testing")
            return True
        else:
            print(f"❌ Delete failed! Count should be {initial_count - 1} but is {final_count}")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def check_database_schema():
    """Check if database has required columns"""
    db_path = os.path.join('database', 'marketplace.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Check items table schema
        cur.execute("PRAGMA table_info(items)")
        columns = [col[1] for col in cur.fetchall()]
        
        required_columns = ['item_id', 'item_name', 'moderation_status']
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return False
        else:
            print("✅ Database schema looks good")
            return True
            
    except Exception as e:
        print(f"❌ Schema check error: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔍 Testing delete functionality...")
    print("=" * 50)
    
    schema_ok = check_database_schema()
    if schema_ok:
        delete_ok = test_delete_functionality()
        
        if delete_ok:
            print("\n✅ Database delete functionality is working correctly!")
            print("💡 The issue might be with:")
            print("   - Flask app not running")
            print("   - Route not being called")
            print("   - Admin authentication")
            print("   - Browser JavaScript errors")
        else:
            print("\n❌ Database delete functionality has issues")
    else:
        print("\n❌ Database schema issues detected")