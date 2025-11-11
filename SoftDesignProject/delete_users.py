import sqlite3

conn = sqlite3.connect('database/marketplace.db')
cursor = conn.cursor()

# List all users
cursor.execute('SELECT student_id, name, email, email_verified FROM students ORDER BY student_id')
users = cursor.fetchall()

print("\n" + "=" * 80)
print("📋 ALL USERS IN DATABASE")
print("=" * 80)

if not users:
    print("No users found.")
else:
    for user in users:
        verified = "✅" if user[3] else "❌"
        print(f"ID: {user[0]:3d} | {user[1]:20s} | {user[2]:35s} | {verified}")

print("=" * 80)
print(f"\nTotal users: {len(users)}")

# Ask which users to delete
print("\n🗑️  DELETE USERS")
print("Enter user IDs to delete (comma-separated, e.g., 2,3,4)")
print("Or press Enter to cancel")

user_input = input("\nIDs to delete: ").strip()

if user_input:
    try:
        ids_to_delete = [int(x.strip()) for x in user_input.split(',')]
        
        for user_id in ids_to_delete:
            cursor.execute('SELECT name, email FROM students WHERE student_id = ?', (user_id,))
            user = cursor.fetchone()
            
            if user:
                cursor.execute('DELETE FROM students WHERE student_id = ?', (user_id,))
                print(f"✅ Deleted: {user[0]} ({user[1]})")
            else:
                print(f"❌ User ID {user_id} not found")
        
        conn.commit()
        
        # Show updated list
        print("\n" + "=" * 80)
        print("📋 UPDATED USER LIST")
        print("=" * 80)
        
        cursor.execute('SELECT student_id, name, email, email_verified FROM students ORDER BY student_id')
        users = cursor.fetchall()
        
        if not users:
            print("No users remaining.")
        else:
            for user in users:
                verified = "✅" if user[3] else "❌"
                print(f"ID: {user[0]:3d} | {user[1]:20s} | {user[2]:35s} | {verified}")
        
        print("=" * 80)
        print(f"\nTotal users: {len(users)}")
        
    except ValueError:
        print("❌ Invalid input. Please enter numbers separated by commas.")
else:
    print("No users deleted.")

conn.close()
