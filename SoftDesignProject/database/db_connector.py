"""
Database utility for connecting to SQLite (local) or PostgreSQL (production)
"""
import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Get database connection - PostgreSQL in production, SQLite locally
    Returns a connection with dictionary cursor
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Production: Use PostgreSQL
        # Render uses postgres:// but psycopg2 needs postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        return conn
    else:
        # Local development: Use SQLite
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'marketplace.db')
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for better concurrency
        conn.execute('PRAGMA journal_mode=WAL;')
        return conn

def init_postgresql_db(conn):
    """
    Initialize PostgreSQL database with all tables
    Call this once when setting up PostgreSQL
    """
    cur = conn.cursor()
    
    # Create students table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email_verified INTEGER DEFAULT 0,
            verification_code TEXT,
            verification_code_expires TIMESTAMP,
            is_admin INTEGER DEFAULT 0
        )
    """)
    
    # Create items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(student_id),
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            contact TEXT,
            payment TEXT,
            status TEXT DEFAULT 'available',
            category TEXT DEFAULT 'other',
            moderation_status TEXT DEFAULT 'approved'
        )
    """)
    
    # Create messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id SERIAL PRIMARY KEY,
            sender_id INTEGER REFERENCES students(student_id),
            receiver_id INTEGER REFERENCES students(student_id),
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read INTEGER DEFAULT 0,
            edited_at TIMESTAMP
        )
    """)
    
    # Create item_images table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS item_images (
            id SERIAL PRIMARY KEY,
            item_id INTEGER NOT NULL REFERENCES items(item_id) ON DELETE CASCADE,
            image_filename TEXT NOT NULL,
            is_primary INTEGER DEFAULT 0,
            upload_order INTEGER DEFAULT 0
        )
    """)
    
    # Create admin_actions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_actions (
            action_id SERIAL PRIMARY KEY,
            admin_id INTEGER REFERENCES students(student_id),
            action_type TEXT,
            target_type TEXT,
            target_id INTEGER,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("✅ PostgreSQL database initialized successfully!")
