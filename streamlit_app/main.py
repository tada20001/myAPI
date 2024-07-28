import streamlit as st
import importlib
import os

def load_apps():
    apps = {}
    apps_dir = os.path.join(os.path.dirname(__file__), 'apps')
    for app_name in os.listdir(apps_dir):
        app_dir = os.path.join(apps_dir, app_name)
        if os.path.isdir(app_dir):
            module_name = f'apps.{app_name}.{app_name}_main'
            module = importlib.import_module(module_name)
            if hasattr(module, 'app'):
                apps[app_name] = module.app
    return apps

def main():
    st.set_page_config(page_title="Dynamic Multi-app Streamlit", layout="wide")

    apps = load_apps()

    # URL에서 앱 파라미터 가져오기
    query_params = st.query_params
    app_name = query_params.get("app", "")

    st.title("Welcome to Dynamic Multi-app Streamlit")

    # 앱 리스트를 중앙에 세로로 배치
    st.subheader("App List")
    if st.button("Home"):
        st.query_params.clear()
        st.rerun()
    
    for name in apps.keys():
        if st.button(name):
            st.query_params["app"] = name
            st.rerun()

    st.markdown("---")

    # 선택된 앱 표시
    if app_name == "":
        st.write("Please select an app from the list above.")
    elif app_name in apps:
        st.subheader(f"Running {app_name}")
        apps[app_name]()
    else:
        st.error(f"App '{app_name}' not found.")

if __name__ == "__main__":
    main()