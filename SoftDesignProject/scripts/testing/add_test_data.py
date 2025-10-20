#!/usr/bin/env python3
"""
Add test items to database for testing delete functionality
"""
import sqlite3
import os

def add_test_items():
    """Add some test items to the database"""
    db_path = os.path.join('database', 'marketplace.db')
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Check if we need a student to associate items with
        cur.execute("SELECT student_id FROM students LIMIT 1")
        student = cur.fetchone()
        
        if not student:
            print("Creating test student...")
            cur.execute("""
                INSERT INTO students (first_name, last_name, email, phone, password_hash, is_admin)
                VALUES ('Test', 'Student', 'test@student.com', '123-456-7890', 'dummy_hash', 0)
            """)
            student_id = cur.lastrowid
        else:
            student_id = student[0]
        
        # Add test items
        test_items = [
            ("Test Textbook", "Introduction to Computer Science textbook", 25.00, "textbook", "pending"),
            ("Used Laptop", "Dell laptop in good condition", 300.00, "electronics", "pending"),
            ("Bicycle", "Mountain bike for campus commute", 150.00, "transportation", "pending"),
            ("Desk Lamp", "Adjustable LED desk lamp", 20.00, "furniture", "approved"),
            ("Calculator", "Scientific calculator TI-84", 75.00, "school_supplies", "rejected")
        ]
        
        for name, desc, price, category, status in test_items:
            cur.execute("""
                INSERT INTO items (student_id, item_name, description, price, category, moderation_status, contact, payment)
                VALUES (?, ?, ?, ?, ?, ?, 'test@student.com', 'cash')
            """, (student_id, name, desc, price, category, status))
        
        conn.commit()
        
        # Check results
        cur.execute("SELECT COUNT(*) FROM items")
        count = cur.fetchone()[0]
        print(f"✅ Added test items successfully! Total items: {count}")
        
        # Show items by status
        cur.execute("SELECT moderation_status, COUNT(*) FROM items GROUP BY moderation_status")
        for row in cur.fetchall():
            print(f"   {row[0]}: {row[1]} items")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding test items: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("🧪 Adding test items to database...")
    print("=" * 40)
    
    success = add_test_items()
    
    if success:
        print("\n✅ Test data ready!")
        print("🌐 Go to: http://localhost:5000/admin")
        print("👤 Login: admin@sea.com / admin123")
        print("🗑️ Try deleting some items!")
    else:
        print("\n❌ Failed to add test data")