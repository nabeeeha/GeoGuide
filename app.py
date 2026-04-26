import streamlit as st
from dotenv import load_dotenv
from auth import register_user, verify_user
from process import read_docs, get_text_chunks, get_vectorstore, get_conversation_chain
from chat import serialize_chat_history, save_chat_history, start_chat_session, display_chat_session
from database import create_users_table, create_chat_sessions_table
import json
from htmlTemplates import css, bot_template, user_template
import time
import os
import pickle
import csv

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state['username'] = username
            st.session_state['chat_history'] = []
            st.session_state['selected_session'] = None
            st.success("Logged in successfully.")
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password.")

def signup():
    st.subheader("Sign up")
    username = st.text_input("Create Username", key='new_user')
    password = st.text_input("Create Password", type="password", key='new_password')
    if st.button("Sign up"):
        if register_user(username, password):
            st.success("User created successfully. Please log in.")
        else:
            st.error("Username already exists.")

def logout():
    if 'username' in st.session_state:
        del st.session_state['username']
    st.experimental_rerun()


def handle_userinput(user_question):
    start_time = time.time()
    response = st.session_state.conversation({'question': user_question})
    
    end_time = time.time()
    duration = end_time - start_time

    if isinstance(response, dict) and 'chat_history' in response:
        st.session_state.chat_history = response['chat_history']
        # Serialize and save the chat history
        serialized_history = serialize_chat_history(st.session_state.chat_history)
        save_chat_history(st.session_state['username'], json.dumps(serialized_history))
    else:
        st.session_state.chat_history = []
        st.error("Failed to retrieve chat history or improper format.")
    
    for i, message in enumerate(st.session_state.chat_history):
        display_message = message.content if hasattr(message, 'content') else "Message format error"
        html_template = user_template if i % 2 == 0 else bot_template
        st.write(html_template.replace("{{MSG}}", display_message), unsafe_allow_html=True)
        
        log_time_to_csv('response_time_openai.csv', 'Response Generation', duration, len(display_message))

def log_time_to_csv(filename, action, duration, chars_count=None):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), action, duration, chars_count if chars_count is not None else 'N/A'])

def main():
    username = st.session_state.get('username', 'User')  # Default to 'User' if not set

    if 'active_session_id' not in st.session_state:
        # Automatically start a new session only if there's no active session
        st.session_state['active_session_id'] = start_chat_session(username)
        display_chat_session(st.session_state['active_session_id'])

    st.header("GeoGuide: A Chatbot for Mining Rules and Regulations :books:")
    user_question = st.chat_input("Ask away your queries:")
    
    intro = "🤖 Hello! I'm GeoGuide, your assistant for Mining Rules and Regulations. Ask me anything about the mining-related laws in India, and I'll do my best to help you."
    st.write(bot_template.replace("{{MSG}}", intro), unsafe_allow_html=True)
    
    if user_question:
        handle_userinput(user_question)
    
    st.sidebar.title(f"Welcome, {username}")

    with st.sidebar:
        if st.button("Start"):
            with st.spinner("Initializing from saved data..."):
                # Load the vector store from a pickle file
                vectorstore_file = 'vectorstore1.pkl'
                if not os.path.exists(vectorstore_file):
                    st.error("Vector store file not found. Please contact the administrator.")
                else:
                    with open(vectorstore_file, 'rb') as file:
                        vectorstore = pickle.load(file)

                    # Create conversation chain from the loaded vector store
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("Chat is ready. Ask your questions!")
            #log_time_to_csv('embedding_time_openai.csv', 'Embedding Generation', duration, total_chars)


def main_auth():
    load_dotenv()
    st.set_page_config(page_title="GeoGuide", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    

    if "username" not in st.session_state:
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
        with login_tab:
            login()
        with signup_tab:
            signup()
    else:
        if st.sidebar.button("Logout"):
            logout()
        main()
        
if __name__ == '__main__':
    create_users_table()
    create_chat_sessions_table()
    main_auth()
