"""
1. /health/ 엔드포인트 구현: Django 백엔드에서 /health/ 엔드포인트 구현.
이 엔드포인트는 서버의 상태를 확인하고, 적절한 응답을 반환해야 함.
2. 로그인 API 구현: Django 백엔드에서 /api/user/login/ 엔드포인트를 구현.
이 엔드포인트는 사용자 인증을 처리하고, 성공 시 토큰을 발급해야 함.
3. 토큰 검증 API 구현: Django 백엔드에서 /api/user/verify/ 엔드포인트를 구현.
이 엔드포인트는 전달받은 토큰의 유효성을 검사하고, 결과를 반환해야 함.
"""
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

# Django 백엔드 URL 설정
# DJANGO_HOST = os.getenv('DJANGO_HOST', 'django_app')
# DJANGO_PORT = os.getenv('DJANGO_PORT', '8000')
# BACKEND_URL = f"http://{DJANGO_HOST}:{DJANGO_PORT}"
BACKEND_URL = "http://localhost:8000/"
# @st.cache_data(ttl=30)  # 30초 동안 결과를 캐시
# def check_api_connection():
#     try:
#         response = requests.get(f"{BACKEND_URL}/health/", timeout=5)
#         return response.status_code == 200
#     except requests.RequestException as e:
#         st.error(f"API Connection Error: {str(e)}")
#         return False
    
    
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
    # 연결 상태 표시
    # if check_api_connection():
    #     st.success("✅ Connected to Django API")
    # else:
    #     st.warning("⚠️ Not connected to Django API")
    #     st.error("Unable to connect to Django API. Please check your network connection or contact support.")
    #     return

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