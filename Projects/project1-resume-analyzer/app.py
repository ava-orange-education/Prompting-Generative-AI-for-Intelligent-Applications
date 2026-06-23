# app.py
# Streamlit interface for the Intelligent Resume Analyzer

import streamlit as st
from resume_analyzer import analyze_resume
import PyPDF2
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# --- App Title and Description ---
st.title("Intelligent Resume Analyzer")
st.write(
    "Upload a resume and paste a job description. "
    "The system will evaluate how well the resume matches the role "
    "using semantic search and AI-powered analysis."
)

st.divider()

# --- Resume Upload ---
st.subheader("Step 1: Upload a Resume")

uploaded_file = st.file_uploader(
    "Upload a resume file (PDF or TXT)",
    type=["pdf", "txt"]
)

resume_text = ""

if uploaded_file is not None:
    # Handle PDF files
    if uploaded_file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            pages = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            resume_text = "\n".join(pages)
        except Exception as e:
            st.error(f"Could not read the PDF file. Error: {e}")

    # Handle TXT files
    elif uploaded_file.type == "text/plain":
        resume_text = uploaded_file.read().decode("utf-8")

    # Show a short preview
    if resume_text.strip():
        st.success("Resume uploaded successfully.")
        with st.expander("Preview resume content"):
            st.write(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))
    else:
        st.warning(
            "The uploaded file appears to be empty or unreadable. "
            "Please check that it contains selectable text."
        )

st.divider()

# --- Job Description Input ---
st.subheader("Step 2: Paste the Job Description")

job_description = st.text_area(
    "Paste the full job description here",
    height=200,
    placeholder="Example: We are looking for a Python developer with 3+ years of experience..."
)

st.divider()

# --- Analyze Button ---
st.subheader("Step 3: Analyze")

analyze_button = st.button("Analyze Resume", type="primary")

if analyze_button:
    # Validate inputs
    if not resume_text.strip():
        st.warning("Please upload a resume before analyzing.")
    elif not job_description.strip():
        st.warning("Please paste a job description before analyzing.")
    elif len(resume_text.split()) < 20:
        st.warning(
            "The resume seems too short for a meaningful analysis. "
            "Please upload a more complete resume."
        )
    elif len(job_description.split()) < 10:
        st.warning(
            "The job description seems too short. "
            "Please provide more details for a better analysis."
        )
    else:
        with st.spinner("Analyzing the resume. This may take a few seconds..."):
            try:
                report = analyze_resume(resume_text, job_description)

                st.divider()
                st.subheader("Evaluation Report")
                st.markdown(report)

            except Exception as e:
                st.error(
                    "Something went wrong during analysis. "
                    "Please check your API key and internet connection."
                )
                st.error(f"Error details: {e}")
