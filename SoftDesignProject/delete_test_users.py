import sqlite3

conn = sqlite3.connect('database/marketplace.db')
cursor = conn.cursor()

# Delete users 1-13
ids_to_delete = list(range(1, 14))
deleted = []

for user_id in ids_to_delete:
    cursor.execute('SELECT name, email FROM students WHERE student_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if user:
        cursor.execute('DELETE FROM students WHERE student_id = ?', (user_id,))
        deleted.append(f"ID {user_id}: {user[0]} ({user[1]})")

conn.commit()

print("✅ Deleted users:")
for u in deleted:
    print(f"  - {u}")

# Show remaining users
cursor.execute('SELECT student_id, name, email, email_verified FROM students ORDER BY student_id')
remaining = cursor.fetchall()

print(f"\n📋 Remaining users: {len(remaining)}")
for u in remaining:
    verified = "✅" if u[3] else "❌"
    print(f"  ID {u[0]}: {u[1]} ({u[2]}) {verified}")

conn.close()
