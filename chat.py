import json
import streamlit as st
from database import create_login_connection


def start_chat_session(username):
    conn = create_login_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO chat_sessions (username, chat_content)
            VALUES (?, ?)
        ''', (username, ''))
        conn.commit()
        return cursor.lastrowid  # Return the session ID of the newly created session
    finally:
        conn.close()
        
def display_chat_session(session_id):
    conn = create_login_connection()
    try:
        session = conn.execute('''
            SELECT chat_content FROM chat_sessions WHERE session_id = ?
        ''', (session_id,)).fetchone()
        if session:
            st.write(session[0])
    finally:
        conn.close()
        
        
def serialize_message(message):
    return {'content': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(message, 'timestamp') else None}

def serialize_chat_history(chat_history):
    return [serialize_message(message) for message in chat_history]

def save_chat_history(username, chat_content):
    conn = create_login_connection()
    try:
        conn.execute('''
            INSERT INTO chat_sessions (username, chat_content)
            VALUES (?, ?)
        ''', (username, chat_content))
        conn.commit()
    finally:
        conn.close()