import sqlite3

def init_db():
    conn = sqlite3.connect('marketplace.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        org TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        image TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

if __name__ == "__main__":
    init_db()
