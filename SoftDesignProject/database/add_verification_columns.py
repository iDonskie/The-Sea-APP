"""
Add email verification columns to students table
"""
import sqlite3
import os

def add_verification_columns():
    db_path = os.path.join(os.path.dirname(__file__), 'marketplace.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check existing columns
        cursor.execute("PRAGMA table_info(students)")
        columns = [row[1] for row in cursor.fetchall()]
        
        changes_made = False
        
        # Add email_verified column
        if 'email_verified' not in columns:
            print("Adding 'email_verified' column...")
            cursor.execute("""
                ALTER TABLE students 
                ADD COLUMN email_verified INTEGER DEFAULT 0
            """)
            changes_made = True
        
        # Add verification_code column
        if 'verification_code' not in columns:
            print("Adding 'verification_code' column...")
            cursor.execute("""
                ALTER TABLE students 
                ADD COLUMN verification_code TEXT DEFAULT NULL
            """)
            changes_made = True
        
        # Add verification_code_expires column
        if 'verification_code_expires' not in columns:
            print("Adding 'verification_code_expires' column...")
            cursor.execute("""
                ALTER TABLE students 
                ADD COLUMN verification_code_expires DATETIME DEFAULT NULL
            """)
            changes_made = True
        
        if changes_made:
            conn.commit()
            print("✅ Successfully added email verification columns!")
        else:
            print("✅ Email verification columns already exist!")
        
        # Show current columns
        cursor.execute("PRAGMA table_info(students)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nCurrent students table columns: {', '.join(columns)}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_verification_columns()
