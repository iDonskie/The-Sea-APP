import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('SoftDesignProject/database/marketplace.db')
cur = conn.cursor()

cur.execute("""
    SELECT student_id, name, email, email_verified, verification_code, verification_code_expires 
    FROM students WHERE email = ?
""", ('almark_occeno@yahoo.com',))

user = cur.fetchone()

if user:
    print(f"User ID: {user[0]}")
    print(f"Name: {user[1]}")
    print(f"Email: {user[2]}")
    print(f"Verified: {user[3]}")
    print(f"Code: {user[4]}")
    print(f"Expires: {user[5]}")
    
    if user[5]:
        exp = datetime.fromisoformat(user[5])
        now = datetime.now()
        print(f"Current time: {now}")
        print(f"Code expired: {now > exp}")
        
        if now > exp:
            print("\n⚠️ Code has expired! Generating new one...")
            new_code = ''.join([str(i) for i in [8,5,8,8,5,0]])
            new_expires = datetime.now() + timedelta(minutes=30)
            cur.execute("""
                UPDATE students 
                SET verification_code = ?, verification_code_expires = ?
                WHERE student_id = ?
            """, (new_code, new_expires, user[0]))
            conn.commit()
            print(f"✅ New verification code: {new_code}")
            print(f"✅ Valid until: {new_expires}")
else:
    print("❌ User not found!")

conn.close()
