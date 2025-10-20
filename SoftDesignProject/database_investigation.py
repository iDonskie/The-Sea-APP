import sqlite3
import os

def check_database(db_path, db_name):
    """Check users in a specific database file"""
    print(f"\n=== CHECKING {db_name.upper()} ===")
    
    if not os.path.exists(db_path):
        print(f"❌ {db_name} does not exist!")
        return []
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Check if students table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        if not cur.fetchone():
            print(f"❌ No 'students' table found in {db_name}")
            return []
        
        # Get all users
        cur.execute('SELECT student_id, name, email, is_admin FROM students')
        users = cur.fetchall()
        
        print(f"📋 Found {len(users)} users in {db_name}:")
        for user in users:
            admin_status = 'ADMIN' if user['is_admin'] else 'USER'
            print(f"  ID: {user['student_id']}, Name: {user['name']}, Email: {user['email']}, Type: {admin_status}")
        
        conn.close()
        return users
        
    except Exception as e:
        print(f"❌ Error with {db_name}: {e}")
        return []

def main():
    print("🔍 DATABASE USER INVESTIGATION")
    print("=" * 50)
    
    # Check both database files
    marketplace_users = check_database('data/marketplace.db', 'marketplace.db')
    database_users = check_database('data/database.db', 'database.db')
    
    print(f"\n📊 SUMMARY:")
    print(f"marketplace.db: {len(marketplace_users)} users")
    print(f"database.db: {len(database_users)} users")
    
    # Check if app.py is using the right database
    print(f"\n🔧 CHECKING APP CONFIGURATION...")
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'marketplace.db' in content:
                print("✅ app.py is configured to use marketplace.db")
            elif 'database.db' in content:
                print("⚠️  app.py is configured to use database.db")
            else:
                print("❓ Could not determine which database app.py uses")
    except Exception as e:
        print(f"❌ Error checking app.py: {e}")

if __name__ == "__main__":
    main()