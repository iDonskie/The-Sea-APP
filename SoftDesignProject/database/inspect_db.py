import sqlite3, os, sys

db = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'marketplace.db')
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row  # <-- This makes rows behave like dicts!
cur = conn.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", tables)

for t in tables:
    print("\n=== SCHEMA for", t, "===\n")
    for row in cur.execute(f"PRAGMA table_info({t})"):
        print(row)
    print("\n--- first 10 rows ---")
    for row in cur.execute(f"SELECT * FROM {t} LIMIT 10"):
        print(dict(row))  # Show keys and values for each row

conn.close()