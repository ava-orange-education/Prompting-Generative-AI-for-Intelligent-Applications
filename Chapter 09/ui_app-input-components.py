import streamlit as st

st.title("Simple Demo")

user_name = st.text_input("Enter your name")
text_data = st.text_area("Paste your content here")
job_role = st.selectbox("Select a job role", ["Developer", "Analyst", "Designer"])
creativity = st.slider("Creativity level", 0, 100, 50)