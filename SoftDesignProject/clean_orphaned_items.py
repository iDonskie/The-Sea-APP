import sqlite3

conn = sqlite3.connect('database/marketplace.db')
cursor = conn.cursor()

print("=" * 80)
print("🧹 CLEANING ORPHANED ITEMS")
print("=" * 80)

# Find orphaned items (items where the owner user no longer exists)
cursor.execute('''
    SELECT i.item_id, i.item_name, i.price, i.student_id
    FROM items i
    LEFT JOIN students s ON i.student_id = s.student_id
    WHERE s.student_id IS NULL
''')
orphaned = cursor.fetchall()

if orphaned:
    print(f"\nFound {len(orphaned)} orphaned items:")
    for item in orphaned:
        print(f"  🗑️  ID {item[0]}: {item[1]} (₱{item[2]:.2f}) - Owner ID {item[3]} (DELETED)")
    
    print("\n" + "=" * 80)
    delete = input("Delete all orphaned items? (yes/no): ").strip().lower()
    
    if delete == 'yes':
        cursor.execute('''
            DELETE FROM items 
            WHERE student_id NOT IN (SELECT student_id FROM students)
        ''')
        conn.commit()
        deleted_count = cursor.rowcount
        print(f"\n✅ Deleted {deleted_count} orphaned items!")
    else:
        print("\n❌ No items deleted.")
else:
    print("\n✅ No orphaned items found!")

# Show remaining items
cursor.execute('''
    SELECT i.item_id, i.item_name, i.price, s.name, s.email
    FROM items i
    JOIN students s ON i.student_id = s.student_id
    ORDER BY i.item_id
''')
remaining = cursor.fetchall()

print("\n" + "=" * 80)
print(f"📦 Remaining items: {len(remaining)}")
print("=" * 80)
for item in remaining:
    print(f"  ID {item[0]}: {item[1]} (₱{item[2]:.2f}) - Owner: {item[3]} ({item[4]})")

conn.close()
