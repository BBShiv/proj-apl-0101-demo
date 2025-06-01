import streamlit as st
import requests

st.title("RAG System Interface")

query = st.text_input("Enter your query:")

if st.button("Submit"):
    if query:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/inference",
                    json={"query": query}
                )
                result = response.json().get("results")
                # print(result)
                st.success(result)
                # print(response.json())
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query.")