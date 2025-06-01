import streamlit as st
import requests

import logging
import apl_logger

logger = logging.getLogger(__name__)

logger.info("Initializing UI...")

st.title("RAG System Interface")

query = st.text_input("Enter your query:")

if st.button("Submit"):
    logger.info("User submitted the query")

    if query:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/inference",
                    json={"query": query}
                )
                result = response.json().get("results")
                # print(result)
                logger.info("Result: %s", result)
                st.success(result)
                # print(response.json())
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query.")
