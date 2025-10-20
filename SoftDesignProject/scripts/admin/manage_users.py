#!/usr/bin/env python3
"""
User Management Tool for Student Emporium
Easy way to manage user accounts and passwords
"""

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import getpass

class UserManager:
    def __init__(self, db_path='data/marketplace.db'):
        self.db_path = db_path
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def list_all_users(self):
        """Show all users in the system"""
        print("\n👥 ALL USERS IN SYSTEM")
        print("=" * 50)
        
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT student_id, name, email, is_admin FROM students ORDER BY student_id')
        users = cur.fetchall()
        conn.close()
        
        if not users:
            print("❌ No users found!")
            return
        
        for user in users:
            user_type = "🔴 ADMIN" if user['is_admin'] else "🔵 USER"
            print(f"ID: {user['student_id']:2} | {user_type} | {user['name']:15} | {user['email']}")
        
        print(f"\nTotal: {len(users)} users")
    
    def reset_user_password(self, email, new_password):
        """Reset a user's password"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT name FROM students WHERE email = ?", (email,))
        user = cur.fetchone()
        
        if not user:
            print(f"❌ User with email '{email}' not found!")
            conn.close()
            return False
        
        # Update password
        hashed_password = generate_password_hash(new_password)
        cur.execute("UPDATE students SET password = ? WHERE email = ?", (hashed_password, email))
        conn.commit()
        conn.close()
        
        print(f"✅ Password updated for {user['name']} ({email})")
        print(f"   New password: {new_password}")
        return True
    
    def create_user(self, name, email, password, is_admin=False):
        """Create a new user"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        # Check if email already exists
        cur.execute("SELECT email FROM students WHERE email = ?", (email,))
        if cur.fetchone():
            print(f"❌ Email '{email}' already exists!")
            conn.close()
            return False
        
        # Create user
        hashed_password = generate_password_hash(password)
        cur.execute("""
            INSERT INTO students (name, email, password, is_admin) 
            VALUES (?, ?, ?, ?)
        """, (name, email, hashed_password, 1 if is_admin else 0))
        
        conn.commit()
        conn.close()
        
        user_type = "admin" if is_admin else "user"
        print(f"✅ Created new {user_type}: {name} ({email})")
        return True
    
    def reset_all_passwords(self, new_password="123"):
        """Reset ALL user passwords to the same simple password"""
        print(f"\n⚠️  RESETTING ALL PASSWORDS TO: '{new_password}'")
        
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT email, name FROM students')
        users = cur.fetchall()
        
        hashed_password = generate_password_hash(new_password)
        cur.execute("UPDATE students SET password = ?", (hashed_password,))
        conn.commit()
        conn.close()
        
        print(f"✅ Reset passwords for {len(users)} users:")
        for user in users:
            print(f"   📧 {user['email']} (Password: {new_password})")

def main():
    manager = UserManager()
    
    while True:
        print("\n🛠️  STUDENT EMPORIUM - USER MANAGER")
        print("=" * 40)
        print("1. 👥 List all users")
        print("2. 🔄 Reset user password")
        print("3. ➕ Create new user")
        print("4. 🔴 Reset ALL passwords to '123'")
        print("5. ❌ Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == '1':
            manager.list_all_users()
        
        elif choice == '2':
            email = input("Enter user email: ").strip()
            password = input("Enter new password: ").strip()
            manager.reset_user_password(email, password)
        
        elif choice == '3':
            name = input("Enter full name: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            is_admin = input("Make admin? (y/n): ").strip().lower() == 'y'
            manager.create_user(name, email, password, is_admin)
        
        elif choice == '4':
            confirm = input("⚠️  Reset ALL passwords to '123'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                manager.reset_all_passwords("123")
            else:
                print("❌ Cancelled")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")

if __name__ == "__main__":
    main()