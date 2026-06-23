from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

question = st.text_input("Ask a question")
if st.button("Ask"):
    llm = OpenAI(api_key=api_key)

    # Send the question to the model
    response = llm.chat.completions.create(model="gpt-4o-mini",
                messages=[{"role": "user", "content": question}])

    # Display the text output
    st.success(response.choices[0].message.content)