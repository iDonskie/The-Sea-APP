import sqlite3
import os

project_root = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(project_root, "marketplace.db")

sql_students = """
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
"""

sql_items = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    item_name TEXT NOT NULL,
    price REAL,
    description TEXT,
    image TEXT,
    contact TEXT,
    payment TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
);
"""

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute(sql_students)
cur.execute(sql_items)
conn.commit()
conn.close()

print("Initialized new DB at:", db_path)