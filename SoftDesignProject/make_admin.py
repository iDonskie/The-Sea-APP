import sqlite3
import os
from werkzeug.security import generate_password_hash

# Get correct database path
db_path = 'database/marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("👑 ADMIN ACCOUNT MANAGER")
print("=" * 60)

# Show current users
cursor.execute('SELECT student_id, name, email, is_admin, email_verified FROM students')
users = cursor.fetchall()

print("\nCurrent users:")
for u in users:
    admin_status = "👑 ADMIN" if u[3] else "👤 User"
    verified = "✅" if u[4] else "❌"
    print(f"  ID {u[0]}: {u[1]} ({u[2]}) - {admin_status} {verified}")

print("\n" + "=" * 60)
print("Options:")
print("1. Make existing user an admin")
print("2. Create new admin account")
print("=" * 60)

choice = input("\nChoose option (1-2): ").strip()

if choice == '1':
    user_id = input("Enter user ID to make admin: ").strip()
    try:
        user_id = int(user_id)
        cursor.execute('SELECT name, email FROM students WHERE student_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            cursor.execute('UPDATE students SET is_admin = 1, email_verified = 1 WHERE student_id = ?', (user_id,))
            conn.commit()
            print(f"\n✅ {user[0]} ({user[1]}) is now an ADMIN!")
            print("✅ Email also verified for convenience")
        else:
            print(f"\n❌ User ID {user_id} not found")
    except ValueError:
        print("❌ Invalid ID")

elif choice == '2':
    print("\n📝 Create New Admin Account")
    name = input("Name: ").strip()
    email = input("Email: ").strip().lower()
    password = input("Password: ").strip()
    
    if name and email and password:
        password_hash = generate_password_hash(password)
        try:
            cursor.execute('''
                INSERT INTO students (name, email, password, is_admin, email_verified)
                VALUES (?, ?, ?, 1, 1)
            ''', (name, email, password_hash))
            conn.commit()
            print(f"\n✅ Admin account created!")
            print(f"   Name: {name}")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Status: 👑 ADMIN")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("❌ All fields are required")

# Show final state
print("\n" + "=" * 60)
print("Updated user list:")
cursor.execute('SELECT student_id, name, email, is_admin FROM students')
users = cursor.fetchall()
for u in users:
    admin_status = "👑 ADMIN" if u[3] else "👤 User"
    print(f"  ID {u[0]}: {u[1]} ({u[2]}) - {admin_status}")

conn.close()
