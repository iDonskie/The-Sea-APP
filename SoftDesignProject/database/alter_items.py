import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "marketplace.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("PRAGMA table_info(items)")
cols = [r[1] for r in cur.fetchall()]
print("Existing columns:", cols)

def try_add(col_sql, name):
    if name not in cols:
        try:
            cur.execute(col_sql)
            print("Added column:", name)
        except sqlite3.OperationalError as e:
            print("Could not add", name, "-", e)

try_add("ALTER TABLE items ADD COLUMN image TEXT", "image")
try_add("ALTER TABLE items ADD COLUMN contact TEXT", "contact")
try_add("ALTER TABLE items ADD COLUMN payment TEXT", "payment")
try_add("ALTER TABLE items ADD COLUMN status TEXT DEFAULT 'available'", "status")

conn.commit()

cur.execute("PRAGMA table_info(items)")
cols2 = [r[1] for r in cur.fetchall()]
print("Updated columns:", cols2)

conn.close()