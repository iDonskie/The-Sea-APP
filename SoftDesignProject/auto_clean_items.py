import sqlite3

conn = sqlite3.connect('database/marketplace.db')
cursor = conn.cursor()

print("🧹 Cleaning orphaned items...")

# Delete orphaned items
cursor.execute('''
    DELETE FROM items 
    WHERE student_id NOT IN (SELECT student_id FROM students)
''')
conn.commit()
deleted_count = cursor.rowcount

print(f"✅ Deleted {deleted_count} orphaned items!")

# Show remaining items
cursor.execute('''
    SELECT i.item_id, i.item_name, i.price, s.name, s.email
    FROM items i
    JOIN students s ON i.student_id = s.student_id
    ORDER BY i.item_id
''')
remaining = cursor.fetchall()

print(f"\n📦 Remaining items: {len(remaining)}")
for item in remaining:
    print(f"  ID {item[0]}: {item[1]} (₱{item[2]:.2f}) - Owner: {item[3]} ({item[4]})")

conn.close()
