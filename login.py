import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import hashlib

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_credentials():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT username, password, email FROM users")
    users = c.fetchall()
    conn.close()
    credentials = {"usernames": {}}
    for username, password, email in users:
        credentials["usernames"][username] = {
            "name": username,
            "password": password,
            "email": email
        }
    return credentials

def register_user(username, password, email):
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
    conn.commit()
    conn.close()

def main():
    st.title("Login")

    # Get user credentials
    credentials = get_user_credentials()

    authenticator = stauth.Authenticate(
        credentials,
        "cookie_name",
        "random_key",
        cookie_expiry_days=30
    )

    fields = ["username", "password"]

    name, authentication_status, username = authenticator.login(fields=fields)

    if authentication_status:
        st.session_state['authentication_status'] = authentication_status
        st.session_state['username'] = username
        st.session_state['name'] = name
        st.success(f"Welcome {name}")
        # Display user options (e.g., go to Home, Portfolio, Simulation)
    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")

    if st.checkbox('Register'):
        st.subheader("Register a new user")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_email = st.text_input("Email")
        if st.button("Register"):
            register_user(new_username, new_password, new_email)
            st.success("User registered successfully")

if __name__ == "__main__":
    main()
