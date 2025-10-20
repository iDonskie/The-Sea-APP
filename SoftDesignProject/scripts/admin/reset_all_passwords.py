import sqlite3
from werkzeug.security import generate_password_hash

# Reset all passwords to "123" for easy login
conn = sqlite3.connect('data/marketplace.db')
cur = conn.cursor()

# Get all users first
cur.execute('SELECT email, name FROM students')
users = cur.fetchall()

# Reset all passwords to "123"
hashed = generate_password_hash("123")
cur.execute("UPDATE students SET password = ?", (hashed,))
conn.commit()
conn.close()

print("✅ ALL PASSWORDS RESET TO: 123")
print("=" * 40)
print("You can now login with ANY email and password '123':")
print()
for email, name in users:
    print(f"📧 {email} | Password: 123")