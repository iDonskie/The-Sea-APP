from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import sqlite3
import os
import uuid
import re
from datetime import datetime, timedelta
import hashlib
import secrets
import random
import string

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration - Use environment variables in production
app.secret_key = os.environ.get('SECRET_KEY', 'your-super-secret-key-change-this-in-production-2024')
is_production = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_SECURE'] = is_production  # True for HTTPS in production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Your email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Your app password
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@sea-marketplace.com')

mail = Mail(app)

# Simple in-memory rate limiting (use Redis in production)
login_attempts = {}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    return True, "Password is valid"

def sanitize_input(text, max_length=500):
    """Sanitize text input"""
    if not text:
        return ""
    # Remove potential HTML/script tags and limit length
    text = re.sub(r'<[^>]*>', '', str(text))
    text = text.strip()[:max_length]
    return text

def validate_file_upload(file):
    """Validate uploaded file"""
    if not file or not file.filename:
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, "File type not allowed. Please upload PNG, JPG, JPEG, or GIF files only"
    
    # Check file size (this is a basic check, file.content_length might not always be available)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
    
    return True, "File is valid"


def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'database', 'marketplace.db')
    # Add timeout and enable WAL mode for better concurrent access
    conn = sqlite3.connect(db_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email, code, name):
    """Send verification code via email with timeout handling"""
    try:
        msg = Message(
            subject="Verify Your Email - SEA Marketplace",
            recipients=[email]
        )
        msg.body = f"""
Hello {name},

Thank you for registering at SEA - Student's Emporium for All!

Your verification code is: {code}

Please enter this code on the verification page to complete your registration.
This code will expire in 15 minutes.

If you didn't create an account, please ignore this email.

Best regards,
SEA Marketplace Team
        """
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px 10px 0 0;">
        <h1 style="color: white; margin: 0;">SEA Marketplace</h1>
    </div>
    <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
        <h2 style="color: #333;">Hello {name},</h2>
        <p style="color: #666; font-size: 16px;">Thank you for registering at SEA - Student's Emporium for All!</p>
        <p style="color: #666; font-size: 16px;">Your verification code is:</p>
        <div style="background: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
            <h1 style="color: #667eea; font-size: 36px; letter-spacing: 8px; margin: 0;">{code}</h1>
        </div>
        <p style="color: #666; font-size: 14px;">Please enter this code on the verification page to complete your registration.</p>
        <p style="color: #999; font-size: 12px; margin-top: 20px;">This code will expire in 15 minutes.</p>
        <p style="color: #999; font-size: 12px;">If you didn't create an account, please ignore this email.</p>
    </div>
</body>
</html>
        """
        # Send email with timeout protection
        with mail.connect() as conn:
            conn.send(msg)
        return True
    except Exception as e:
        # Log error but don't crash - user can still use resend button
        print(f"Error sending email to {email}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def require_login():
    """Check if user is logged in and session is valid"""
    if 'user_id' not in session:
        return False
    
    # Check session timeout (optional - 24 hour sessions)
    if 'last_activity' in session:
        try:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if datetime.now() - last_activity > timedelta(hours=24):
                session.clear()
                return False
        except:
            pass
    
    # Update last activity
    session['last_activity'] = datetime.now().isoformat()
    return True

def generate_csrf_token():
    """Generate a CSRF token for the current session"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

def validate_csrf_token(token):
    """Validate CSRF token"""
    return token and session.get('csrf_token') == token

@app.context_processor
def inject_csrf_token():
    """Make CSRF token available in templates"""
    return dict(csrf_token=generate_csrf_token)

@app.context_processor
def inject_admin_status():
    """Make admin status available in all templates"""
    return dict(is_admin_user=is_admin())

def is_admin():
    """Check if current user is an admin"""
    if not require_login():
        return False
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT is_admin FROM students WHERE student_id = ?", (session['user_id'],))
    result = cur.fetchone()
    conn.close()
    
    return result and result[0] == 1

def require_admin():
    """Decorator to require admin access"""
    if not is_admin():
        flash("Access denied. Admin privileges required.", "error")
        return redirect(url_for('home'))
    return True

def log_admin_action(action_type, target_type, target_id, details=None, conn=None):
    """Log admin actions for audit trail"""
    if not require_login():
        return
    
    # Use provided connection or create a new one
    if conn is None:
        conn = get_db_connection()
        should_close = True
    else:
        should_close = False
    
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO admin_actions (admin_id, action_type, target_type, target_id, details)
        VALUES (?, ?, ?, ?, ?)
    """, (session['user_id'], action_type, target_type, target_id, details))
    
    if should_close:
        conn.commit()
        conn.close()


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # CSRF Protection
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf_token(csrf_token):
            flash("Security token invalid. Please try again.")
            return render_template('register.html')
        
        # Get and sanitize input
        name = sanitize_input(request.form.get('name', ''), 100)
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        # Validation
        if not (name and email and password):
            flash("Please fill all required fields.")
            return render_template('register.html')
        
        if len(name) < 2:
            flash("Name must be at least 2 characters long.")
            return render_template('register.html')
            
        if not validate_email(email):
            flash("Please enter a valid email address.")
            return render_template('register.html')
            
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message)
            return render_template('register.html')
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Generate verification code
        verification_code = generate_verification_code()
        code_expires = datetime.now() + timedelta(minutes=15)
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # Insert new user with verification code
            cur.execute("""
                INSERT INTO students (name, email, password, email_verified, verification_code, verification_code_expires) 
                VALUES (?, ?, ?, 0, ?, ?)
            """, (name, email, password_hash, verification_code, code_expires))
            conn.commit()
            user_id = cur.lastrowid
            
            # Send verification email
            email_sent = send_verification_email(email, verification_code, name)
            
            if email_sent:
                # Store user_id in session for verification
                session['pending_verification_user_id'] = user_id
                session['pending_verification_email'] = email
                flash("Registration successful! Please check your email for the verification code.", "success")
                return redirect(url_for('verify_email'))
            else:
                # If email fails, still allow registration but notify user
                flash("Registration successful but we couldn't send the verification email. You can request a new code.", "warning")
                session['pending_verification_user_id'] = user_id
                session['pending_verification_email'] = email
                return redirect(url_for('verify_email'))
                
        except sqlite3.IntegrityError:
            flash("Email already registered. Please use a different email.")
            return render_template('register.html')
        except Exception as e:
            print(f"Registration error: {e}")
            flash("An error occurred during registration. Please try again.")
            return render_template('register.html')
        finally:
            conn.close()
    return render_template('register.html')


@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    """Verify email with code sent to user"""
    if 'pending_verification_user_id' not in session:
        flash("No pending verification. Please register first.")
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        
        if not code:
            flash("Please enter the verification code.")
            return render_template('verify_email.html')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            user_id = session['pending_verification_user_id']
            cur.execute("""
                SELECT verification_code, verification_code_expires, email_verified 
                FROM students WHERE student_id = ?
            """, (user_id,))
            user = cur.fetchone()
            
            if not user:
                flash("User not found. Please register again.")
                return redirect(url_for('register'))
            
            # Check if already verified
            if user['email_verified']:
                flash("Email already verified. Please log in.", "success")
                session.pop('pending_verification_user_id', None)
                session.pop('pending_verification_email', None)
                return redirect(url_for('login'))
            
            # Check if code matches
            if user['verification_code'] != code:
                flash("Invalid verification code. Please try again.")
                return render_template('verify_email.html')
            
            # Check if code expired
            expires = datetime.fromisoformat(user['verification_code_expires'])
            if datetime.now() > expires:
                flash("Verification code expired. Please request a new one.")
                return render_template('verify_email.html', expired=True)
            
            # Verify the email
            cur.execute("""
                UPDATE students 
                SET email_verified = 1, verification_code = NULL, verification_code_expires = NULL
                WHERE student_id = ?
            """, (user_id,))
            conn.commit()
            
            flash("Email verified successfully! You can now log in.", "success")
            session.pop('pending_verification_user_id', None)
            session.pop('pending_verification_email', None)
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"Verification error: {e}")
            flash("An error occurred during verification. Please try again.")
            return render_template('verify_email.html')
        finally:
            conn.close()
    
    return render_template('verify_email.html', email=session.get('pending_verification_email'))

@app.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification code"""
    if 'pending_verification_user_id' not in session:
        flash("No pending verification. Please register first.")
        return redirect(url_for('register'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        user_id = session['pending_verification_user_id']
        cur.execute("SELECT name, email FROM students WHERE student_id = ?", (user_id,))
        user = cur.fetchone()
        
        if not user:
            flash("User not found. Please register again.")
            return redirect(url_for('register'))
        
        # Generate new code
        verification_code = generate_verification_code()
        code_expires = datetime.now() + timedelta(minutes=15)
        
        # Update database
        cur.execute("""
            UPDATE students 
            SET verification_code = ?, verification_code_expires = ?
            WHERE student_id = ?
        """, (verification_code, code_expires, user_id))
        conn.commit()
        
        # Send email
        if send_verification_email(user['email'], verification_code, user['name']):
            flash("Verification code sent! Please check your email.", "success")
        else:
            flash("Failed to send email. Please try again later.", "error")
        
        return redirect(url_for('verify_email'))
        
    except Exception as e:
        print(f"Resend error: {e}")
        flash("An error occurred. Please try again.")
        return redirect(url_for('verify_email'))
    finally:
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        # Basic validation
        if not email or not password:
            flash("Please enter both email and password.")
            return render_template('login.html')
        
        if not validate_email(email):
            flash("Please enter a valid email address.")
            return render_template('login.html')
        
        # Rate limiting: Check failed login attempts
        client_ip = request.remote_addr
        current_time = datetime.now()
        
        # Clean old attempts (older than 15 minutes)
        if client_ip in login_attempts:
            login_attempts[client_ip] = [
                attempt_time for attempt_time in login_attempts[client_ip] 
                if current_time - attempt_time < timedelta(minutes=15)
            ]
        
        # Check if too many attempts
        if client_ip in login_attempts and len(login_attempts[client_ip]) >= 5:
            flash("Too many failed login attempts. Please try again in 15 minutes.")
            return render_template('login.html')
        
        # CSRF Protection
        csrf_token = request.form.get('csrf_token')
        if not csrf_token:
            flash("Security token missing. Please refresh the page and try again.")
            return render_template('login.html')
        if not validate_csrf_token(csrf_token):
            flash("Security token invalid. Please refresh the page and try again.")
            return render_template('login.html')
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT student_id, name, password, email_verified FROM students WHERE email=?", (email,))
            user = cur.fetchone()
            
            if user and check_password_hash(user['password'], password):
                # Check if email is verified
                if not user['email_verified']:
                    flash("Please verify your email before logging in. Check your inbox for the verification code.", "warning")
                    session['pending_verification_user_id'] = user['student_id']
                    session['pending_verification_email'] = email
                    return redirect(url_for('verify_email'))
                
                # Clear failed attempts on successful login
                if client_ip in login_attempts:
                    del login_attempts[client_ip]
                    
                # Regenerate session ID to prevent session fixation
                session.permanent = True
                app.permanent_session_lifetime = timedelta(hours=24)
                session['user_id'] = user['student_id']
                session['user_name'] = user['name']
                session['last_activity'] = datetime.now().isoformat()
                flash("Welcome back!")
                return redirect(url_for('marketplace'))
            else:
                # Record failed attempt
                if client_ip not in login_attempts:
                    login_attempts[client_ip] = []
                login_attempts[client_ip].append(current_time)
                
                flash("Invalid email or password.")
                return render_template('login.html')
        except Exception as e:
            flash("An error occurred during login. Please try again.")
            return render_template('login.html')
        finally:
            conn.close()
    
    # GET request - ensure CSRF token is generated
    generate_csrf_token()  # This will create the token in session if it doesn't exist
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
    
    # Get current user information if logged in
    current_user = None
    if session.get('user_id'):
        cur.execute("SELECT name FROM students WHERE student_id = ?", (session.get('user_id'),))
        user_row = cur.fetchone()
        if user_row:
            current_user = dict(user_row)
    
    # Get items with seller information (filter by moderation status for non-admins)
    if is_admin():
        # Admins can see all items
        cur.execute("""
            SELECT items.*, students.name AS seller_name
            FROM items
            LEFT JOIN students ON items.student_id = students.student_id
            ORDER BY items.item_id DESC
        """)
    else:
        # Regular users only see approved items
        cur.execute("""
            SELECT items.*, students.name AS seller_name
            FROM items
            LEFT JOIN students ON items.student_id = students.student_id
            WHERE items.moderation_status = 'approved'
            ORDER BY items.item_id DESC
        """)
    rows = cur.fetchall()
    items = [dict(r) for r in rows]
    
    # Get images for each item
    for item in items:
        cur.execute("""
            SELECT image_filename, is_primary, upload_order
            FROM item_images 
            WHERE item_id = ? 
            ORDER BY upload_order ASC
        """, (item['item_id'],))
        images = cur.fetchall()
        item['images'] = [dict(img) for img in images]
        
        # Set primary image (for backward compatibility with old image field)
        if item['images']:
            item['primary_image'] = item['images'][0]['image_filename']
        elif item.get('image'):  # Fallback to old image field if exists
            item['primary_image'] = item['image']
        else:
            item['primary_image'] = None
    
    conn.close()
    return render_template('marketplace.html', items=items, current_user=current_user)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if not require_login():
        flash("You must be logged in to add items.")
        return redirect(url_for('login'))
        
    student_id = session.get('user_id')

    if request.method == 'POST':
        # CSRF Protection
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf_token(csrf_token):
            flash("Security token invalid. Please try again.")
            return render_template('add_item.html')
        
        # Get and sanitize input
        item_name = sanitize_input(request.form.get('item_name'), 100)
        price_str = request.form.get('price', '').strip()
        description = sanitize_input(request.form.get('description'), 1000)
        contact = sanitize_input(request.form.get('contact'), 200)
        payment = sanitize_input(request.form.get('payment'), 200)
        category = request.form.get('category', 'other')
        
        # Validation
        if not item_name or len(item_name) < 2:
            flash("Item name must be at least 2 characters long.")
            return render_template('add_item.html')
        
        # Validate price
        try:
            price = float(price_str)
            if price <= 0 or price > 999999:
                flash("Please enter a valid price between 0.01 and 999,999.")
                return render_template('add_item.html')
        except ValueError:
            flash("Please enter a valid price.")
            return render_template('add_item.html')
            
        # Validate category
        valid_categories = ['books', 'electronics', 'supplies', 'appliances', 'clothing', 'food', 'other']
        if category not in valid_categories:
            category = 'other'

        # Handle multiple image files with security validation
        image_files = request.files.getlist('images')
        saved_images = []
        
        if len(image_files) > 5:
            flash("Maximum 5 images allowed.")
            return render_template('add_item.html')
        
        for i, image_file in enumerate(image_files):
            if image_file and image_file.filename:
                is_valid, error_msg = validate_file_upload(image_file)
                if not is_valid:
                    flash(f"Image {i+1}: {error_msg}")
                    return render_template('add_item.html')
                    
                orig = secure_filename(image_file.filename)
                # Create unique filename with timestamp for extra security
                unique = f"{uuid.uuid4().hex}_{int(datetime.now().timestamp())}_{orig}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
                
                try:
                    image_file.save(save_path)
                    saved_images.append((unique, i == 0))  # (filename, is_primary)
                except Exception as e:
                    flash(f"Error saving image {i+1}. Please try again.")
                    return render_template('add_item.html')

        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Insert the item using parameterized query to prevent SQL injection
            # New items are approved by default (you can change this to 'pending' if you want moderation)
            moderation_status = 'approved'  # Change to 'pending' if you want admin approval required
            cur.execute(
                "INSERT INTO items (student_id, item_name, price, description, contact, payment, status, category, moderation_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (student_id, item_name, price, description, contact, payment, 'available', category, moderation_status)
            )
            
            item_id = cur.lastrowid
            
            # Insert images into the item_images table
            for i, (filename, is_primary) in enumerate(saved_images):
                cur.execute(
                    "INSERT INTO item_images (item_id, image_filename, is_primary, upload_order) VALUES (?, ?, ?, ?)",
                    (item_id, filename, 1 if is_primary else 0, i + 1)
                )
            conn.commit()
            if is_admin():
                flash("Item added successfully and approved!", "success")
            else:
                flash("Item added successfully! It's pending approval and will appear in the marketplace once reviewed.", "success")
            return redirect(url_for('marketplace'))
        except Exception as e:
            conn.rollback()
            flash("Error adding item. Please try again.")
            return render_template('add_item.html')
        finally:
            conn.close()

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
    
    # Get images for each item
    for item in items:
        cur.execute("""
            SELECT image_filename, is_primary, upload_order
            FROM item_images 
            WHERE item_id = ? 
            ORDER BY upload_order ASC
        """, (item['item_id'],))
        images = cur.fetchall()
        item['images'] = [dict(img) for img in images]
        
        # Set primary image
        if item['images']:
            item['primary_image'] = item['images'][0]['image_filename']
        elif item.get('image'):  # Fallback to old image field
            item['primary_image'] = item['image']
        else:
            item['primary_image'] = None
    
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
        category = request.form.get('category', 'other')

        # Handle multiple image files
        image_files = request.files.getlist('images')
        if image_files and any(f.filename for f in image_files):
            # Delete old images first
            cur.execute("SELECT image_filename FROM item_images WHERE item_id = ?", (item_id,))
            old_images = cur.fetchall()
            for old_img in old_images:
                try:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_img['image_filename'])
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass
            
            # Delete old image records
            cur.execute("DELETE FROM item_images WHERE item_id = ?", (item_id,))
            
            # Add new images
            saved_images = []
            for i, image_file in enumerate(image_files):
                if image_file and image_file.filename:
                    if not allowed_file(image_file.filename):
                        flash(f"Invalid file type for image {i+1}.")
                        conn.close()
                        return render_template('edit_listing.html', item=item)
                    orig = secure_filename(image_file.filename)
                    unique = f"{uuid.uuid4().hex}_{orig}"
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
                    image_file.save(save_path)
                    saved_images.append((unique, i == 0))  # (filename, is_primary)
            
            # Insert new images into the item_images table
            for i, (filename, is_primary) in enumerate(saved_images):
                cur.execute(
                    "INSERT INTO item_images (item_id, image_filename, is_primary, upload_order) VALUES (?, ?, ?, ?)",
                    (item_id, filename, 1 if is_primary else 0, i + 1)
                )

        cur.execute(
            "UPDATE items SET item_name=?, price=?, description=?, contact=?, payment=?, status=?, category=? WHERE item_id=?",
            (item_name, price, description, contact, payment, status, category, item_id)
        )
        conn.commit()
        conn.close()
        flash("Listing updated!", "success")
        return redirect(url_for('my_listings'))

    # Get existing images for this item
    cur.execute("""
        SELECT image_filename, is_primary, upload_order
        FROM item_images 
        WHERE item_id = ? 
        ORDER BY upload_order ASC
    """, (item_id,))
    images = cur.fetchall()
    item['images'] = [dict(img) for img in images]
    
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
        SELECT s.student_id, s.name, m2.content AS last_msg, t.last_at
        FROM (
            SELECT other_id, MAX(last_msg) AS last_at
            FROM (
                SELECT receiver_id AS other_id, created_at AS last_msg FROM messages WHERE sender_id=?
                UNION ALL
                SELECT sender_id   AS other_id, created_at AS last_msg FROM messages WHERE receiver_id=?
            )
            GROUP BY other_id
        ) t
        JOIN messages m2 ON (
            (m2.sender_id = ? AND m2.receiver_id = t.other_id AND m2.created_at = t.last_at)
            OR
            (m2.sender_id = t.other_id AND m2.receiver_id = ? AND m2.created_at = t.last_at)
        )
        JOIN students s ON s.student_id = t.other_id
        WHERE t.other_id != ?
        ORDER BY t.last_at DESC
    """, (user_id, user_id, user_id, user_id, user_id))
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
    return render_template('chat.html', other=dict(other), other_id=other_id, user_id=user_id)


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
        # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename and allowed_file(image_file.filename):
                orig = secure_filename(image_file.filename)
                unique = f"{uuid.uuid4().hex}_{orig}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
                image_file.save(save_path)
                
                # Insert image message
                cur.execute("INSERT INTO messages (sender_id, receiver_id, content, image_attachment, message_type) VALUES (?, ?, ?, ?, ?)",
                           (user_id, other_id, "📸 Image", unique, "image"))
                conn.commit()
                conn.close()
                return jsonify({"ok": True}), 201
            else:
                conn.close()
                return jsonify({"error": "invalid image file"}), 400
        
        # Handle text message
        print(f"[DEBUG] Received text message request from user {user_id} to {other_id}")
        data = request.get_json() or {}
        print(f"[DEBUG] Request data: {data}")
        content = (data.get('content') or "").strip()
        print(f"[DEBUG] Message content: '{content}'")
        if not content:
            print("[DEBUG] Empty message content, rejecting")
            conn.close()
            return jsonify({"error": "empty message"}), 400
        cur.execute("INSERT INTO messages (sender_id, receiver_id, content, message_type) VALUES (?, ?, ?, ?)",
                    (user_id, other_id, content, "text"))
        conn.commit()
        conn.close()
        return jsonify({"ok": True}), 201
    
    # Try to get messages with edited_at column, fallback if column doesn't exist
    try:
        cur.execute("""
            SELECT id, sender_id, receiver_id, content, created_at, is_read, image_attachment, message_type, edited_at
            FROM messages
            WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
            ORDER BY created_at ASC
        """, (user_id, other_id, other_id, user_id))
    except sqlite3.OperationalError:
        # Fallback for tables without edited_at column
        cur.execute("""
            SELECT id, sender_id, receiver_id, content, created_at, is_read, image_attachment, message_type
            FROM messages
            WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
            ORDER BY created_at ASC
        """, (user_id, other_id, other_id, user_id))
    
    rows = cur.fetchall()
    cur.execute("UPDATE messages SET is_read=1 WHERE receiver_id=? AND sender_id=? AND is_read=0", (user_id, other_id))
    conn.commit()
    
    msgs = []
    for r in rows:
        msg = {
            "id": r["id"], 
            "sender_id": r["sender_id"], 
            "receiver_id": r["receiver_id"],
            "content": r["content"], 
            "created_at": r["created_at"], 
            "is_read": r["is_read"],
            "image_attachment": r["image_attachment"], 
            "message_type": r["message_type"] or "text",
            "edited": False  # Default value
        }
        # Try to get edited_at if column exists
        try:
            msg["edited"] = bool(r["edited_at"])
        except (KeyError, IndexError):
            pass  # Use default value
        msgs.append(msg)
    
    conn.close()
    return jsonify(msgs)


@app.route('/chat/message/<int:message_id>', methods=['PUT', 'DELETE'])
def edit_delete_message(message_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "login required"}), 401
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if message exists and belongs to the user
    cur.execute("SELECT sender_id, content, image_attachment FROM messages WHERE id = ?", (message_id,))
    message = cur.fetchone()
    
    if not message:
        conn.close()
        return jsonify({"error": "message not found"}), 404
    
    if message['sender_id'] != user_id:
        conn.close()
        return jsonify({"error": "unauthorized"}), 403
    
    if request.method == 'DELETE':
        # Delete the message
        cur.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
        
        # Also delete the image file if it exists
        if message['image_attachment']:
            try:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], message['image_attachment'])
                if os.path.exists(image_path):
                    os.remove(image_path)
            except Exception as e:
                print(f"Error deleting image file: {e}")
        
        conn.close()
        return jsonify({"ok": True, "action": "deleted"})
    
    elif request.method == 'PUT':
        # Edit the message (only for text messages)
        data = request.get_json() or {}
        new_content = (data.get('content') or "").strip()
        
        if not new_content:
            conn.close()
            return jsonify({"error": "empty message"}), 400
        
        # Only allow editing text messages
        cur.execute("SELECT message_type FROM messages WHERE id = ?", (message_id,))
        msg_type = cur.fetchone()
        if msg_type and msg_type['message_type'] == 'image':
            conn.close()
            return jsonify({"error": "cannot edit image messages"}), 400
        
        # Update message and set edited_at timestamp
        cur.execute("UPDATE messages SET content = ?, edited_at = CURRENT_TIMESTAMP WHERE id = ?", (new_content, message_id))
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "action": "edited", "new_content": new_content})


# New Chat API Routes
@app.route('/api/chat/<int:other_id>/messages')
def api_get_messages(other_id):
    """Get messages between current user and another user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "login required"}), 401
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Mark messages as read
        cur.execute("UPDATE messages SET is_read = 1 WHERE sender_id = ? AND receiver_id = ?", (other_id, user_id))
        
        # Get messages (handle missing columns gracefully)
        try:
            cur.execute("""
                SELECT id, sender_id, receiver_id, content, created_at, message_type, 
                       image_attachment, deleted, edited_at
                FROM messages
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                ORDER BY created_at ASC
            """, (user_id, other_id, other_id, user_id))
        except sqlite3.OperationalError:
            # Fallback for missing columns
            cur.execute("""
                SELECT id, sender_id, receiver_id, content, created_at, message_type, 
                       image_attachment
                FROM messages
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                ORDER BY created_at ASC
            """, (user_id, other_id, other_id, user_id))
        
        messages = []
        for row in cur.fetchall():
            # Handle both old and new table structures
            message = {
                'id': row['id'],
                'sender_id': row['sender_id'],
                'receiver_id': row['receiver_id'],
                'content': row['content'],
                'created_at': row['created_at'],
                'type': row['message_type'] or 'text',
                'image_url': row['image_attachment'],
                'deleted': False,  # Default for old tables
                'edited': False    # Default for old tables
            }
            
            # Try to get deleted/edited info if columns exist
            try:
                message['deleted'] = bool(row['deleted'])
                message['edited'] = bool(row['edited_at'])
            except (KeyError, IndexError):
                pass  # Use defaults
            
            messages.append(message)
        
        conn.commit()
        conn.close()
        return jsonify(messages)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/<int:other_id>/send', methods=['POST'])
def api_send_message(other_id):
    """Send a message to another user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "login required"}), 401
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if other user exists
        cur.execute("SELECT student_id FROM students WHERE student_id = ?", (other_id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"error": "user not found"}), 404
        
        # Handle image upload
        if 'image' in request.files:
            print(f"[DEBUG] Processing image upload from user {user_id} to {other_id}")
            image_file = request.files['image']
            if image_file and image_file.filename:
                try:
                    filename = secure_filename(image_file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    
                    print(f"[DEBUG] Saving image to: {save_path}")
                    
                    # Create directory if it doesn't exist
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    image_file.save(save_path)
                    
                    print(f"[DEBUG] Image saved successfully")
                    
                    # Save image message
                    cur.execute("""
                        INSERT INTO messages (sender_id, receiver_id, content, message_type, image_attachment)
                        VALUES (?, ?, ?, ?, ?)
                    """, (user_id, other_id, "📸 Image", "image", unique_filename))
                    
                    conn.commit()
                    conn.close()
                    print(f"[DEBUG] Image message saved to database")
                    return jsonify({"ok": True, "type": "image"})
                    
                except Exception as img_error:
                    print(f"[ERROR] Image upload failed: {img_error}")
                    conn.close()
                    return jsonify({"error": f"Image upload failed: {str(img_error)}"}), 500
            else:
                conn.close()
                return jsonify({"error": "No valid image file"}), 400
        
        # Handle text message
        print(f"[DEBUG] Processing text message from user {user_id} to {other_id}")
        data = request.get_json()
        print(f"[DEBUG] Received JSON data: {data}")
        
        if not data or not data.get('content'):
            print("[DEBUG] No data or no content in request")
            conn.close()
            return jsonify({"error": "empty message"}), 400
        
        content = data['content'].strip()
        print(f"[DEBUG] Message content: '{content}'")
        
        if not content:
            print("[DEBUG] Empty content after strip")
            conn.close()
            return jsonify({"error": "empty message"}), 400
        
        # Save text message
        print(f"[DEBUG] Saving text message to database")
        cur.execute("""
            INSERT INTO messages (sender_id, receiver_id, content, message_type)
            VALUES (?, ?, ?, ?)
        """, (user_id, other_id, content, "text"))
        
        conn.commit()
        conn.close()
        print(f"[DEBUG] Text message saved successfully")
        return jsonify({"ok": True, "type": "text"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/message/<int:message_id>/edit', methods=['PUT'])
def api_edit_message(message_id):
    """Edit a message"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "login required"}), 401
    
    try:
        data = request.get_json()
        new_content = data.get('content', '').strip()
        
        if not new_content:
            return jsonify({"error": "empty message"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if message exists and belongs to user
        cur.execute("SELECT sender_id, message_type FROM messages WHERE id = ?", (message_id,))
        message = cur.fetchone()
        
        if not message:
            conn.close()
            return jsonify({"error": "message not found"}), 404
        
        if message['sender_id'] != user_id:
            conn.close()
            return jsonify({"error": "unauthorized"}), 403
        
        if message['message_type'] == 'image':
            conn.close()
            return jsonify({"error": "cannot edit image messages"}), 400
        
        # Update message (handle missing edited_at column)
        try:
            cur.execute("""
                UPDATE messages 
                SET content = ?, edited_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (new_content, message_id))
        except sqlite3.OperationalError:
            # Fallback: just update content
            cur.execute("UPDATE messages SET content = ? WHERE id = ?", (new_content, message_id))
        
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "new_content": new_content})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/message/<int:message_id>/delete', methods=['DELETE'])
def api_delete_message(message_id):
    """Delete (mark as deleted) a message"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "login required"}), 401
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if message exists and belongs to user
        cur.execute("SELECT sender_id FROM messages WHERE id = ?", (message_id,))
        message = cur.fetchone()
        
        if not message:
            conn.close()
            return jsonify({"error": "message not found"}), 404
        
        if message['sender_id'] != user_id:
            conn.close()
            return jsonify({"error": "unauthorized"}), 403
        
        # Mark as deleted instead of actually deleting (handle missing column)
        try:
            cur.execute("""
                UPDATE messages 
                SET deleted = 1, content = 'This message was deleted'
                WHERE id = ?
            """, (message_id,))
        except sqlite3.OperationalError:
            # Fallback: actually delete if no deleted column
            cur.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    """Admin dashboard showing all listings for moderation"""
    if not require_admin():
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get all items with user info
    cur.execute("""
        SELECT i.*, s.name as seller_name, s.email as seller_email,
               (SELECT COUNT(*) FROM admin_actions WHERE target_type='item' AND target_id=i.item_id) as action_count
        FROM items i 
        JOIN students s ON i.student_id = s.student_id 
        ORDER BY i.item_id DESC
    """)
    
    items = [dict(row) for row in cur.fetchall()]
    
    # Get moderation statistics
    cur.execute("SELECT moderation_status, COUNT(*) as count FROM items GROUP BY moderation_status")
    stats = dict(cur.fetchall())
    
    conn.close()
    
    return render_template('admin/dashboard.html', items=items, stats=stats)

@app.route('/admin/moderate/<int:item_id>/<action>', methods=['GET', 'POST'])
def moderate_item(item_id, action):
    """Moderate an item (approve/reject/suspend/delete)"""
    print(f"[DEBUG] moderate_item called with item_id={item_id}, action={action}")
    if not require_admin():
        print("[DEBUG] User not admin, redirecting to home")
        return redirect(url_for('home'))
    
    valid_actions = ['approve', 'reject', 'suspend', 'delete']
    if action not in valid_actions:
        flash("Invalid moderation action.", "error")
        return redirect(url_for('admin_dashboard'))
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get item info for logging
        cur.execute("SELECT item_name, student_id FROM items WHERE item_id = ?", (item_id,))
        item = cur.fetchone()
        
        if not item:
            flash("Item not found.", "error")
            return redirect(url_for('admin_dashboard'))
        
        if action == 'delete':
            # Delete the item completely
            print(f"[DEBUG] Deleting item {item_id}: {item[0]}")
            cur.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
            log_admin_action('delete', 'item', item_id, f"Deleted item: {item[0]}", conn=conn)
            flash(f"Item '{item[0]}' has been deleted.", "success")
            print(f"[DEBUG] Item {item_id} deleted successfully")
        else:
            # Update moderation status
            cur.execute("UPDATE items SET moderation_status = ? WHERE item_id = ?", (action + 'd', item_id))
            log_admin_action('moderate', 'item', item_id, f"Status changed to: {action}d", conn=conn)
            flash(f"Item '{item[0]}' has been {action}d.", "success")
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"[ERROR] Database error in moderate_item: {e}")
        flash("Database error occurred. Please try again.", "error")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"[ERROR] Unexpected error in moderate_item: {e}")
        flash("An unexpected error occurred. Please try again.", "error")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users')
def admin_users():
    """Admin page for managing users"""
    if not require_admin():
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get all users with their listing counts
    cur.execute("""
        SELECT s.*, 
               COUNT(i.item_id) as item_count,
               COUNT(CASE WHEN i.moderation_status = 'pending' THEN 1 END) as pending_items
        FROM students s 
        LEFT JOIN items i ON s.student_id = i.student_id 
        GROUP BY s.student_id 
        ORDER BY s.student_id DESC
    """)
    
    users = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/promote/<int:user_id>')
def promote_user(user_id):
    """Promote a user to admin"""
    if not require_admin():
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get user info
    cur.execute("SELECT name, email FROM students WHERE student_id = ?", (user_id,))
    user = cur.fetchone()
    
    if not user:
        flash("User not found.", "error")
    else:
        cur.execute("UPDATE students SET is_admin = 1 WHERE student_id = ?", (user_id,))
        conn.commit()
        log_admin_action('promote', 'user', user_id, f"Promoted {user[0]} to admin")
        flash(f"User '{user[0]}' has been promoted to admin.", "success")
    
    conn.close()
    return redirect(url_for('admin_users'))

@app.route('/admin/logs')
def admin_logs():
    """View admin action logs"""
    if not require_admin():
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT aa.*, s.name as admin_name 
        FROM admin_actions aa 
        JOIN students s ON aa.admin_id = s.student_id 
        ORDER BY aa.timestamp DESC 
        LIMIT 100
    """)
    
    logs = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    return render_template('admin/logs.html', logs=logs)


if __name__ == "__main__":
    app.run(debug=True)