from flask import Flask, render_template, request, redirect, url_for, flash, session
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

@app.route('/marketplace')
def marketplace():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    conn.close()
    return render_template('marketplace.html', items=items)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    student_id = session.get('user_id')
    if not student_id:
        flash("You must be logged in to add items.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form['item_name']
        price = request.form['price']
        description = request.form['description']
        contact = request.form['contact']
        payment = request.form['payment']

        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_filename = filename

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (student_id, item_name, price, description, image, contact, payment) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student_id, item_name, price, description, image_filename, contact, payment)
        )
        conn.commit()
        conn.close()

        flash("✅ Item added successfully!")
        return redirect(url_for('marketplace'))

    return render_template('add_item.html')

if __name__ == "__main__":
    app.run(debug=True)