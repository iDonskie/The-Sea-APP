import sqlite3
import os

try:
    conn = sqlite3.connect('data/marketplace.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Check all users
    cur.execute('SELECT student_id, name, email, is_admin FROM students')
    users = cur.fetchall()
    print('=== ALL USERS IN DATABASE ===')
    if users:
        for user in users:
            admin_status = 'ADMIN' if user['is_admin'] else 'USER'
            print(f'ID: {user["student_id"]}, Name: {user["name"]}, Email: {user["email"]}, Type: {admin_status}')
    else:
        print('No users found in database!')
    
    print(f'\nTotal users: {len(users)}')
    conn.close()
except Exception as e:
    print(f'Error: {e}')