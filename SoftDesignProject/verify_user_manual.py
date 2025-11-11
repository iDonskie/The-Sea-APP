import sqlite3

# Connect to database
conn = sqlite3.connect('database/marketplace.db')
cursor = conn.cursor()

# Update the user to verified
cursor.execute('UPDATE students SET email_verified = 1 WHERE email = ?', ('almark.occeno@gmail.com',))
conn.commit()

# Check the result
cursor.execute('SELECT name, email, email_verified FROM students WHERE email = ?', ('almark.occeno@gmail.com',))
user = cursor.fetchone()

if user:
    print(f'✅ User verified successfully!')
    print(f'   Name: {user[0]}')
    print(f'   Email: {user[1]}')
    print(f'   Verified: {"Yes" if user[2] else "No"}')
else:
    print('❌ User not found')

conn.close()
