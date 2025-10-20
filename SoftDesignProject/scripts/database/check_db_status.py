#!/usr/bin/env python3
"""
Check database status and unlock if needed
"""
import os
import sqlite3
import time

def check_database_status():
    """Check if database is accessible and unlock if needed"""
    db_path = os.path.join('database', 'marketplace.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False
    
    print(f"📊 Checking database: {db_path}")
    
    # Check for lock files
    lock_files = [
        db_path + '-journal',
        db_path + '-wal',
        db_path + '-shm'
    ]
    
    for lock_file in lock_files:
        if os.path.exists(lock_file):
            print(f"⚠️  Lock file found: {lock_file}")
            file_size = os.path.getsize(lock_file)
            print(f"   Size: {file_size} bytes")
    
    try:
        # Test connection with timeout
        conn = sqlite3.connect(db_path, timeout=5.0)
        conn.execute('PRAGMA journal_mode=WAL;')
        
        # Try a simple query
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM items")
        count = cur.fetchone()[0]
        print(f"✅ Database accessible. Item count: {count}")
        
        # Check for any open transactions
        cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        print("✅ WAL checkpoint completed")
        
        conn.close()
        return True
        
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print(f"🔒 Database is locked: {e}")
            print("💡 Trying to resolve...")
            
            # Wait a moment for any processes to finish
            time.sleep(2)
            
            # Try again with different connection settings
            try:
                conn = sqlite3.connect(db_path, timeout=30.0)
                conn.execute('PRAGMA journal_mode=WAL;')
                conn.execute('PRAGMA wal_checkpoint(TRUNCATE);')
                conn.close()
                print("✅ Lock resolved!")
                return True
            except Exception as e2:
                print(f"❌ Could not resolve lock: {e2}")
                return False
        else:
            print(f"❌ Database error: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Database Status Check")
    print("=" * 40)
    
    success = check_database_status()
    
    if success:
        print("\n✅ Database is ready for use!")
    else:
        print("\n❌ Database has issues that need attention")
        print("\n💡 Possible solutions:")
        print("   1. Stop all Flask apps and restart")
        print("   2. Restart your computer")
        print("   3. Check for other database connections")