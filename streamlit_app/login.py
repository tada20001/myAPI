import os
from dotenv import load_dotenv
import streamlit as st
import requests
import importlib

# 환경 변수 로드
if os.path.exists('.env.streamlit.dev'):
    load_dotenv('.env.streamlit.dev')
else:
    load_dotenv('.env.streamlit.prod')

BACKEND_URL = os.getenv('DJANGO_BACKEND_URL')

def login():
    st.title("Login")
    email = st.text_input("Email", placeholder="Enter your email address",
        help="Please enter the email address you used to register.")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/user/login/",
                data={"email": email, "password": password}
            )
            response.raise_for_status()
            data = response.json()
            st.session_state.token = data["token"]
            st.session_state.user_email = email
            st.success("Logged in successfully!")
            st.experimental_rerun()
        except requests.RequestException as e:
            st.error(f"Login failed: {str(e)}")

def verify_token():
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/user/verify/",
            headers={"Authorization": f"Token {st.session_state.token}"}
        )
        return response.status_code == 200
    except:
        return False

def load_main_app():
    try:
        main_module = importlib.import_module('main')
        return main_module.main
    except ImportError:
        st.error("Failed to load main application. Please check if main.py exists.")
        return None

def main():
    if "token" not in st.session_state or not verify_token():
        login()
    else:
        main_app = load_main_app()
        if main_app:
            main_app()
        else:
            st.write(f"Welcome, {st.session_state.user_email}!")
            st.write("Main application not available.")

if __name__ == "__main__":
    main()