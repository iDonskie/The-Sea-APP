"""
Fix database by adding email verification columns
"""
import sqlite3
import os

def fix_database():
    # Use the database in the current directory (where the app runs)
    db_path = 'marketplace.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check existing columns
        cursor.execute("PRAGMA table_info(students)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Current columns: {', '.join(columns)}")
        
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
        
        # Show updated columns
        cursor.execute("PRAGMA table_info(students)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nUpdated students table columns: {', '.join(columns)}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_database()
