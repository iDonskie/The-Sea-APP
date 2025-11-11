import sqlite3

conn = sqlite3.connect('database/marketplace.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]

print("📋 Database tables:")
for table in tables:
    print(f"  - {table}")

print("\n📊 Items table structure:")
cursor.execute("PRAGMA table_info(items)")
columns = cursor.fetchall()
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# Check if item_images table exists
if 'item_images' in tables:
    print("\n🖼️ item_images table structure:")
    cursor.execute("PRAGMA table_info(item_images)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
else:
    print("\n❌ item_images table NOT FOUND - this is the problem!")

conn.close()
