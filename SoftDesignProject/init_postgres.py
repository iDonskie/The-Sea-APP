"""
Initialize PostgreSQL database on Render
Run this once after deploying to create all tables
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connector import get_db_connection, init_postgresql_db

if __name__ == '__main__':
    print("🔧 Initializing PostgreSQL database...")
    
    if not os.environ.get('DATABASE_URL'):
        print("❌ DATABASE_URL not found. Make sure you're running this on Render or set DATABASE_URL environment variable.")
        sys.exit(1)
    
    try:
        conn = get_db_connection()
        init_postgresql_db(conn)
        conn.close()
        print("✅ Database initialized successfully!")
        print("You can now use the application.")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
