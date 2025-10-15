import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "marketplace.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER DEFAULT 0,
    FOREIGN KEY(sender_id) REFERENCES students(student_id),
    FOREIGN KEY(receiver_id) REFERENCES students(student_id)
);
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_messages_pair ON messages(sender_id, receiver_id)")
cur.execute("CREATE INDEX IF NOT EXISTS idx_messages_receiver ON messages(receiver_id)")

conn.commit()
conn.close()
print("messages table ensured at", db_path)