import streamlit as st

st.title("Simple Demo")

col1, col2 = st.columns(2)

with col1:
    st.write("Left side")
    st.text_input("Type here")

with col2:
    st.write("Right side")
    st.text_input("Type here also")

