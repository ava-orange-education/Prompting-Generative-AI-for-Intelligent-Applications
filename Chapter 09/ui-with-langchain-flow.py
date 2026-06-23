from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

prompt = ChatPromptTemplate.from_template(
    "Summarise this text: {text}"
)

user_text = st.text_area("Paste your text here")

if st.button("Run"):
    if user_text.strip():
        # Create final messages for the model
        messages = prompt.format_messages(text=user_text)

        # Invoke LLM with the messages list
        result = model.invoke(messages)

        st.write(result.content)
    else:
        st.warning("Please enter some text.")



