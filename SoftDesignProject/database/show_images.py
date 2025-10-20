import os, sqlite3
db = r"c:/Users/almar/Desktop/Codings/Sea_App/SoftDesignProject/database/marketplace.db"
uploads = r"c:/Users/almar/Desktop/Codings/Sea_App/SoftDesignProject/static/uploads"

print("Uploads folder exists:", os.path.exists(uploads))
try:
    files = os.listdir(uploads)
except Exception as e:
    files = ["<error listing folder: %s>" % e]
print("Files in uploads:", files or ["<empty>"])

conn = sqlite3.connect(db)
cur = conn.cursor()
print("\nLast 10 items from DB (item_id, item_name, image, student_id):")
for row in cur.execute("SELECT item_id, item_name, image, student_id FROM items ORDER BY item_id DESC LIMIT 10"):
    item_id, name, img, sid = row
    exists = os.path.exists(os.path.join(uploads, img)) if img else False
    print(f"{item_id}\t{name!r}\timage={img!r}\texists_on_disk={exists}\tseller={sid}")
conn.close()