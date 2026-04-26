import bcrypt
from database import create_login_connection

def register_user(username, password):
    conn = create_login_connection()
    try:
        if conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone():
            return False
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return True
    finally:
        conn.close()

def verify_user(username, password):
    conn = create_login_connection()
    try:
        user = conn.execute('SELECT password_hash FROM users WHERE username = ?', (username,)).fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return True
        return False
    finally:
        conn.close()