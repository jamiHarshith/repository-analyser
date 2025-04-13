# app.py
import streamlit as st
from query_handler import handle_query 

st.title("Codebase analyser")

user_q = st.text_input("Ask a question:")

if user_q:

    response = handle_query(user_q)
    st.write(response.response)
