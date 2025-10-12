import sqlite3
db_path = "c:/Users/almar/Desktop/Codings/Sea_App/SoftDesignProject/database/marketplace.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE items ADD COLUMN contact TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists
try:
    cur.execute("ALTER TABLE items ADD COLUMN payment TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists
conn.commit()
conn.close()
print("Columns 'contact' and 'payment' added if missing.")