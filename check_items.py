import sqlite3

conn = sqlite3.connect('SoftDesignProject/database/marketplace.db')
cur = conn.cursor()

# Check items
cur.execute('SELECT item_id, student_id, item_name, price, description FROM items ORDER BY item_id DESC LIMIT 5')
items = cur.fetchall()

print(f'Total items found: {len(items)}')
if items:
    for item in items:
        print(f'\nItem ID: {item[0]}')
        print(f'Student ID: {item[1]}')
        print(f'Name: {item[2]}')
        print(f'Price: {item[3]}')
        print(f'Description: {item[4][:50] if item[4] else "None"}...')
else:
    print('No items found in database')

conn.close()
