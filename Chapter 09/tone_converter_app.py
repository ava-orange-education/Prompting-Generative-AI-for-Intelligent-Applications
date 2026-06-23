from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)
st.title("AI Tone Converter")
st.write("Transform your text into any tone you need.")

original_text = st.text_area("Paste your text here", height=200)

tone = st.radio(
    "Select the tone you want",
    ["Formal", "Casual", "Friendly", "Persuasive"]
)

convert = st.button("Convert Tone")

if convert:
    if not original_text.strip():
        st.warning("Please paste some text before converting.")
    else:
        with st.spinner("Converting tone..."):
            prompt = f"""
            You are a helpful writing assistant.
            Rewrite the following text in a {tone.lower()} tone.
            Keep the same meaning and main points, but adjust the style and word choice.
            
            Original text:
            {original_text}
            """

            response = client.chat.completions.create(model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}])

            converted_text = response.choices[0].message.content

            st.success("Conversion complete!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Original Text")
                st.write(original_text)
            
            with col2:
                st.markdown("### Converted Text")
                st.write(converted_text)
            st.info("Tip: Try converting the same text into different tones to see how word choice affects meaning.")

