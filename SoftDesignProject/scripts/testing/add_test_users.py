import sqlite3
from werkzeug.security import generate_password_hash

def create_test_users():
    """Create some test users for the marketplace"""
    
    test_users = [
        {
            'name': 'John Smith', 
            'email': 'john@student.com', 
            'password': 'password123',
            'is_admin': 0
        },
        {
            'name': 'Sarah Johnson', 
            'email': 'sarah@student.com', 
            'password': 'password123',
            'is_admin': 0
        },
        {
            'name': 'Mike Wilson', 
            'email': 'mike@student.com', 
            'password': 'password123',
            'is_admin': 0
        },
        {
            'name': 'Emma Brown', 
            'email': 'emma@student.com', 
            'password': 'password123',
            'is_admin': 0
        },
        {
            'name': 'Alex Davis', 
            'email': 'alex@student.com', 
            'password': 'password123',
            'is_admin': 0
        }
    ]
    
    try:
        conn = sqlite3.connect('data/marketplace.db')
        cur = conn.cursor()
        
        print("Creating test users...")
        
        for user in test_users:
            # Check if user already exists
            cur.execute("SELECT email FROM students WHERE email = ?", (user['email'],))
            if cur.fetchone():
                print(f"⚠️  User {user['email']} already exists, skipping...")
                continue
            
            # Hash the password
            hashed_password = generate_password_hash(user['password'])
            
            # Insert the user
            cur.execute("""
                INSERT INTO students (name, email, password, is_admin) 
                VALUES (?, ?, ?, ?)
            """, (user['name'], user['email'], hashed_password, user['is_admin']))
            
            print(f"✅ Created user: {user['name']} ({user['email']})")
        
        conn.commit()
        conn.close()
        
        print(f"\n🎉 Test users created successfully!")
        print(f"\n📋 Login credentials (all passwords are 'password123'):")
        print("="*50)
        for user in test_users:
            print(f"Name: {user['name']}")
            print(f"Email: {user['email']}")
            print(f"Password: {user['password']}")
            print("-" * 30)
            
    except Exception as e:
        print(f'❌ Error creating users: {e}')

if __name__ == "__main__":
    create_test_users()