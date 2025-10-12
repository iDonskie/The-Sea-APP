import os, shutil

db_path = os.path.join(os.path.dirname(__file__), "marketplace.db")
bak_path = db_path + ".badbak"

# if file doesn't exist nothing to do
if not os.path.exists(db_path):
    print("No marketplace.db file found at", db_path)
    raise SystemExit

with open(db_path, "rb") as f:
    header = f.read(16)

if header != b"SQLite format 3\x00":
    print("marketplace.db is NOT a valid SQLite DB — backing up to", bak_path)
    shutil.copy2(db_path, bak_path)
    os.remove(db_path)
    print("Removed invalid marketplace.db (backed up).")
else:
    print("marketplace.db looks like a valid SQLite DB.")