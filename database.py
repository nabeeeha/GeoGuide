import sqlite3

def create_login_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_users_table():
    conn = create_login_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL PRIMARY KEY,
                password_hash TEXT NOT NULL
            );
        ''')
        conn.commit()
    finally:
        conn.close()

def create_chat_sessions_table():
    conn = create_login_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                chat_content TEXT,
                FOREIGN KEY (username) REFERENCES users(username)
            );
        ''')
        conn.commit()
    finally:
        conn.close()