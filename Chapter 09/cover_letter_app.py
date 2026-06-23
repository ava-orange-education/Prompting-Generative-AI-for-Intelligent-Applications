from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

st.title("AI Cover Letter Generator")
st.write("Paste your resume and select a role to generate a cover letter.")

resume_text = st.text_area("Paste your resume here", height=250)

job_role = st.selectbox(
    "Select the job role",
    ["Software Developer", "Business Analyst", "Data Engineer", "Product Manager"]
)

tone = st.radio("Choose the tone of the cover letter", ["Formal", "Friendly", "Confident"])

generate = st.button("Generate Cover Letter")

if generate:
    if not resume_text.strip():
        st.warning("Please paste your resume before generating the cover letter.")
    else:
        with st.spinner("Creating your cover letter..."):
            prompt = f"""
                You are a helpful assistant that writes {tone.lower()} cover letters.
                Write a cover letter for the role of {job_role}.
                Use the following resume as the main source of information.
                Resume:
                {resume_text}
                """
            response = client.chat.completions.create(model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}])

            cover_letter = response.choices[0].message.content

            st.success("Your cover letter is ready.")
            st.markdown("### Generated Cover Letter")
            st.write(cover_letter)

