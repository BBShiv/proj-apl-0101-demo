import streamlit as st
import requests
import ui

# User logs in and gets a JWT from backend
if 'jwt' not in st.session_state:
    username = st.text_input("username")
    password = st.text_input("password", type="password")
    if st.button("Login"):
        res = requests.post("http://localhost:5000/login", json={
            "username": username,
            "password": password
        })
        if res.status_code == 200:
            st.session_state.jwt = res.json()['access_token']
            st.success(ui.main())
            # st.success("Logged in successfully!")





# if st.button("Logout"):
#     st.session_state.pop("jwt", None)
#     st.success("Logged out!")