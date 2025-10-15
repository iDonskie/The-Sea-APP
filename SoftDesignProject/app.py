# ...existing code...
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "dev"

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'marketplace.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not (name and email and password):
            flash("Please fill all required fields.")
            return render_template('register.html')

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
                        (name, email, password))
            conn.commit()
            flash("Registered successfully.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.")
            return render_template('register.html')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['student_id']
            session['user_name'] = user['name']
            flash("Login successful!")
            return redirect(url_for('marketplace'))
        else:
            flash("Invalid email or password.")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/marketplace')
def marketplace():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT items.*, students.name AS seller_name
        FROM items
        LEFT JOIN students ON items.student_id = students.student_id
        ORDER BY items.item_id DESC
    """)
    items = cur.fetchall()
    conn.close()
    return render_template('marketplace.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    student_id = session.get('user_id')
    if not student_id:
        flash("You must be logged in to add items.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            item_name = request.form.get('item_name')
            price = request.form.get('price')
            description = request.form.get('description')
            contact = request.form.get('contact')
            payment = request.form.get('payment')

            image_file = request.files.get('image')
            image_filename = None
            if image_file and image_file.filename and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                image_filename = filename

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (student_id, item_name, price, description, image, contact, payment, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (student_id, item_name, price, description, image_filename, contact, payment, 'available')
            )
            conn.commit()
            conn.close()

            flash("✅ Item added successfully!")
            return redirect(url_for('marketplace'))
        except Exception as e:
            flash(f"Error: {e}")
            return render_template('add_item.html')

    return render_template('add_item.html')

@app.route('/my_listings')
def my_listings():
    student_id = session.get('user_id')
    if not student_id:
        flash("Please log in to view your listings.")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE student_id=?", (student_id,))
    my_items = cur.fetchall()
    conn.close()
    return render_template('my_listings.html', items=my_items)

@app.route('/edit_listing/<int:item_id>', methods=['GET', 'POST'])
def edit_listing(item_id):
    student_id = session.get('user_id')
    if not student_id:
        flash("Please log in to edit listings.")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE item_id=? AND student_id=?", (item_id, student_id))
    item = cur.fetchone()
    if not item:
        conn.close()
        flash("Listing not found or not yours.")
        return redirect(url_for('my_listings'))

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        description = request.form.get('description')
        contact = request.form.get('contact')
        payment = request.form.get('payment')
        status = request.form.get('status')

        cur.execute(
            "UPDATE items SET item_name=?, price=?, description=?, contact=?, payment=?, status=? WHERE item_id=?",
            (item_name, price, description, contact, payment, status, item_id)
        )
        conn.commit()
        conn.close()
        flash("Listing updated!")
        return redirect(url_for('my_listings'))

    conn.close()
    return render_template('edit_listing.html', item=item)

# Ensure old 'conversations' endpoint used by templates doesn't break:
@app.route('/conversations')
def conversations():
    return redirect(url_for('messages'))

# -----------------------
# Messages page (aggregates all conversation partners)
# -----------------------
@app.route('/messages')
def messages():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.name, MAX(m.last_msg) AS last_msg
        FROM (
            SELECT receiver_id AS other_id, created_at AS last_msg FROM messages WHERE sender_id=?
            UNION ALL
            SELECT sender_id   AS other_id, created_at AS last_msg FROM messages WHERE receiver_id=?
        ) m
        JOIN students s ON s.student_id = m.other_id
        WHERE m.other_id != ?
        GROUP BY s.student_id, s.name
        ORDER BY last_msg DESC
    """, (session.get('user_id'), session.get('user_id'), session.get('user_id')))
    convos = cur.fetchall()
    conn.close()
    return render_template('messages.html', convos=convos)

# -----------------------
# Chat page and messages API
# -----------------------
@app.route('/chat/<int:other_id>')
def chat_page(other_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in.")
        return redirect(url_for('login'))
    if other_id == user_id:
        flash("Cannot chat with yourself.")
        return redirect(url_for('messages'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id, name FROM students WHERE student_id=?", (other_id,))
    other = cur.fetchone()
    conn.close()
    if not other:
        flash("User not found.")
        return redirect(url_for('messages'))
    return render_template('chat.html', other=other)

@app.route('/chat/<int:other_id>/messages', methods=['GET', 'POST'])
def chat_messages(other_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "login required"}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    # ensure other exists
    cur.execute("SELECT student_id FROM students WHERE student_id=?", (other_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({"error": "user not found"}), 404

    if request.method == 'POST':
        data = request.get_json() or {}
        content = (data.get('content') or "").strip()
        if not content:
            conn.close()
            return jsonify({"error": "empty message"}), 400
        cur.execute(
            "INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
            (user_id, other_id, content)
        )
        conn.commit()
        conn.close()
        return jsonify({"ok": True}), 201

    # GET messages between two users
    cur.execute("""
        SELECT id, sender_id, receiver_id, content, created_at, is_read
        FROM messages
        WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
        ORDER BY created_at ASC
    """, (user_id, other_id, other_id, user_id))
    rows = cur.fetchall()

    # mark incoming as read
    cur.execute("""
        UPDATE messages SET is_read=1
        WHERE receiver_id=? AND sender_id=? AND is_read=0
    """, (user_id, other_id))
    conn.commit()

    msgs = []
    for r in rows:
        msgs.append({
            "id": r["id"],
            "sender_id": r["sender_id"],
            "receiver_id": r["receiver_id"],
            "content": r["content"],
            "created_at": r["created_at"],
            "is_read": r["is_read"]
        })

    conn.close()
    return jsonify(msgs)

if __name__ == "__main__":
    app.run(debug=True)
