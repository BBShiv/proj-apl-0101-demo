import streamlit as st
import requests
import logging

import apl_logger

logger = logging.getLogger(__name__)

logger.info("Initializing UI...")

# --- Configuration ---
BACKEND_AUTH_URL = "http://127.0.0.1:5000" # Flask authentication backend URL
RAG_INFERENCE_URL = "http://127.0.0.1:5000/inference" # RAG inference API

# --- Session State for Authentication ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'jwt_token' not in st.session_state:
    st.session_state.jwt_token = None
if 'username' not in st.session_state:
    st.session_state.username = None

def login_page():
    st.title("Login to RAG System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            try:
                response = requests.post(
                    f"{BACKEND_AUTH_URL}/login",
                    json={"username": username, "password": password}
                )
                if response.status_code == 200:
                    token = response.json().get('token')
                    st.session_state.logged_in = True
                    st.session_state.jwt_token = token
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                    st.rerun() # Rerun to switch to the main app
                else:
                    st.error(f"Login failed: {response.json().get('message', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the authentication server. Please ensure the backend is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred during login: {e}")
        else:
            st.warning("Please enter both username and password.")

    st.markdown("---")
    st.subheader("New User? Register here!")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

    if st.button("Register"):
        if new_username and new_password and confirm_password:
            if new_password == confirm_password:
                try:
                    response = requests.post(
                        f"{BACKEND_AUTH_URL}/register",
                        json={"username": new_username, "password": new_password}
                    )
                    if response.status_code == 201:
                        st.success("Registration successful! You can now log in.")
                    else:
                        st.error(f"Registration failed: {response.json().get('message', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the authentication server. Please ensure the backend is running.")
                except Exception as e:
                    st.error(f"An unexpected error occurred during registration: {e}")
            else:
                st.warning("Passwords do not match.")
        else:
            st.warning("Please fill in all registration fields.")

def main_app():
    st.title("RAG System Interface")

    st.write(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.jwt_token = None
        st.session_state.username = None
        st.rerun() # Rerun to go back to login page

    query = st.text_input("Enter your query:")

    if st.button("Submit"):
        logger.info("User submitted the query")

        if query:
            with st.spinner("Processing..."):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.jwt_token}"}
                    response = requests.post(
                        RAG_INFERENCE_URL,
                        json={"query": query},
                        headers=headers # Send JWT token with the request
                    )
                    if response.status_code == 200:
                        result = response.json().get("results")
                        logger.info("Result: %s", result)
                        st.success(result)
                    elif response.status_code == 401:
                        st.error("Unauthorized: Your session may have expired. Please log in again.")
                        st.session_state.logged_in = False # Force re-login
                        st.session_state.jwt_token = None
                        st.rerun()
                    else:
                        st.error(f"Error from RAG API: {response.status_code} - {response.json().get('message', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the RAG inference server. Please ensure it's running.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a query.")

# --- Main App Logic ---
if st.session_state.logged_in:
    main_app()
else:
    login_page()