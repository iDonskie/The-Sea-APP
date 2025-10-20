from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os
import uuid

app = Flask(__name__)
app.secret_key = "dev"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'database', 'marketplace.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.template_filter('php')
def format_php(value):
    """Jinja filter: {{ value|php }} -> ₱1,234.56"""
    try:
        if value is None or value == '':
            return ''
        s = str(value).strip()
        s = s.replace(',', '').replace('₱', '').replace('PHP', '').strip()
        v = float(s)
        return f"₱{v:,.2f}"
    except Exception:
        return value


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
    rows = cur.fetchall()
    items = [dict(r) for r in rows]
    conn.close()
    return render_template('marketplace.html', items=items)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    student_id = session.get('user_id')
    if not student_id:
        flash("You must be logged in to add items.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        description = request.form.get('description')
        contact = request.form.get('contact')
        payment = request.form.get('payment')

        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename:
            if not allowed_file(image_file.filename):
                flash("Invalid file type.")
                return render_template('add_item.html')
            orig = secure_filename(image_file.filename)
            unique = f"{uuid.uuid4().hex}_{orig}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
            image_file.save(save_path)
            image_filename = unique

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items (student_id, item_name, price, description, image, contact, payment, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (student_id, item_name, price, description, image_filename, contact, payment, 'available')
        )
        conn.commit()
        conn.close()
        flash("Item added successfully!")
        return redirect(url_for('marketplace'))

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
    rows = cur.fetchall()
    items = [dict(r) for r in rows]
    conn.close()
    return render_template('my_listings.html', items=items)


@app.route('/edit_listing/<int:item_id>', methods=['GET', 'POST'])
def edit_listing(item_id):
    student_id = session.get('user_id')
    if not student_id:
        flash("Please log in to edit listings.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE item_id=? AND student_id=?", (item_id, student_id))
    row = cur.fetchone()
    if not row:
        conn.close()
        flash("Listing not found or not yours.")
        return redirect(url_for('my_listings'))

    item = dict(row)

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        description = request.form.get('description')
        contact = request.form.get('contact')
        payment = request.form.get('payment')
        status = request.form.get('status', 'available')

        image_file = request.files.get('image')
        new_image = item.get('image')
        if image_file and image_file.filename:
            if not allowed_file(image_file.filename):
                flash("Invalid image type.")
                conn.close()
                return render_template('edit_listing.html', item=item)
            orig = secure_filename(image_file.filename)
            unique = f"{uuid.uuid4().hex}_{orig}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
            image_file.save(save_path)
            old = item.get('image')
            if old and old != unique:
                try:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], old)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass
            new_image = unique

        cur.execute(
            "UPDATE items SET item_name=?, price=?, description=?, contact=?, payment=?, status=?, image=? WHERE item_id=?",
            (item_name, price, description, contact, payment, status, new_image, item_id)
        )
        conn.commit()
        conn.close()
        flash("Listing updated!")
        return redirect(url_for('my_listings'))

    conn.close()
    return render_template('edit_listing.html', item=item)


@app.route('/delete_listing/<int:item_id>', methods=['POST'])
def delete_listing(item_id):
    student_id = session.get('user_id')
    if not student_id:
        flash("Please log in.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id, image FROM items WHERE item_id=?", (item_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        flash("Listing not found.")
        return redirect(url_for('my_listings'))

    if row['student_id'] != student_id:
        conn.close()
        flash("You can only remove your own listings.")
        return redirect(url_for('my_listings'))

    img = row['image']
    if img:
        try:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img)
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception:
            pass

    cur.execute("DELETE FROM items WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()
    flash("Listing removed.")
    return redirect(url_for('my_listings'))


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
    """, (user_id, user_id, user_id))
    rows = cur.fetchall()
    convos = [dict(r) for r in rows]
    conn.close()
    return render_template('messages.html', convos=convos)


@app.route('/conversations')
def conversations():
    return redirect(url_for('messages'))


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
    return render_template('chat.html', other=dict(other))


@app.route('/chat/<int:other_id>/messages', methods=['GET', 'POST'])
def chat_messages(other_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "login required"}), 401
    conn = get_db_connection()
    cur = conn.cursor()
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
        cur.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
                    (user_id, other_id, content))
        conn.commit()
        conn.close()
        return jsonify({"ok": True}), 201
    cur.execute("""
        SELECT id, sender_id, receiver_id, content, created_at, is_read
        FROM messages
        WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
        ORDER BY created_at ASC
    """, (user_id, other_id, other_id, user_id))
    rows = cur.fetchall()
    cur.execute("UPDATE messages SET is_read=1 WHERE receiver_id=? AND sender_id=? AND is_read=0", (user_id, other_id))
    conn.commit()
    msgs = [{"id": r["id"], "sender_id": r["sender_id"], "receiver_id": r["receiver_id"],
             "content": r["content"], "created_at": r["created_at"], "is_read": r["is_read"]} for r in rows]
    conn.close()
    return jsonify(msgs)


if __name__ == "__main__":
    app.run(debug=True)