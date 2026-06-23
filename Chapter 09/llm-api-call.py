import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain LLM
client = OpenAI(api_key=api_key)

st.title("Summary Generator")

prompt = st.text_area("Enter your text")

if st.button("Generate Summary"):
    if prompt.strip():
        
        response = client.chat.completions.create(model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}])

        st.write(response.choices[0].message.content)
    else:
        st.warning("Please enter some text.")

