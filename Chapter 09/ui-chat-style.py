import streamlit as st

st.title("Chat with the AI")

user_input = st.text_input("Type your message")

if st.button("Send"):
    st.write("You:", user_input)
    st.write("AI:", "This is a sample AI reply")
