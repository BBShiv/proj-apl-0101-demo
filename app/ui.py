import streamlit as st
import requests



# def app():
#     st.write("Welcome to the RAG System Interface!")
#     st.write("Please enter your query below:")




def main():
    # Use token to call protected endpoint
    if 'jwt' in st.session_state:
        if st.button("Call Protected API"):
            headers = {
                "Authorization": f"Bearer {st.session_state.jwt}"
            }
    st.title("RAG System Interface")
    query = st.text_input("Enter your query:")

    
    if st.button("Submit"):
        if query:
            with st.spinner("Processing..."):
                try:
                    response = requests.post(             #Response will carry jwt token
                        "http://127.0.0.1:5000/inference", 
                        headers=headers,
                        json={"query": query}             #Replace query by username & password
                    )
                    result = response.json().get("results")
                    print(result)
                    st.success(result)
                    # print(response.json())
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a query.")


if __name__ == "__main__":
    main()
    # app()  # Uncomment this line if you want to run the app function



        # res = requests.get("http://localhost:5000/protected", headers=headers)
        # st.write(res.json())