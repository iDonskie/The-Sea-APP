import sqlite3

conn = sqlite3.connect('database/marketplace.db')
cursor = conn.cursor()

# Make user 15 an admin
cursor.execute('UPDATE students SET is_admin = 1, email_verified = 1 WHERE student_id = 15')
conn.commit()

# Verify the change
cursor.execute('SELECT student_id, name, email, is_admin, email_verified FROM students WHERE student_id = 15')
user = cursor.fetchone()

if user:
    print("✅ User updated successfully!")
    print(f"   ID: {user[0]}")
    print(f"   Name: {user[1]}")
    print(f"   Email: {user[2]}")
    print(f"   Admin: {'👑 YES' if user[3] else 'No'}")
    print(f"   Verified: {'✅ YES' if user[4] else 'No'}")
    print("\n🎉 You can now log in as admin with this account!")
else:
    print("❌ User not found")

# Show all users
print("\n" + "=" * 60)
print("All users:")
cursor.execute('SELECT student_id, name, email, is_admin FROM students')
users = cursor.fetchall()
for u in users:
    admin = "👑 ADMIN" if u[3] else "👤 User"
    print(f"  ID {u[0]}: {u[1]} ({u[2]}) - {admin}")

conn.close()
