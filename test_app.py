import streamlit as st
from main import answer_what_if_question

# Test the what-if question functionality
st.title("Test What-If Question")

user_q = st.text_input("Enter a what-if question:")
if st.button("Test Question"):
    if user_q:
        with st.spinner("Testing..."):
            try:
                reply = answer_what_if_question(user_q)
                st.success("Response:")
                st.write(reply)
            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)
    else:
        st.warning("Please enter a question") 