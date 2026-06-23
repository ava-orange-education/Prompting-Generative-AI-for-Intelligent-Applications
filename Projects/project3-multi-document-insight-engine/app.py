# app.py
# Streamlit interface for the Multi-Document Insight Engine

import streamlit as st
from document_engine import process_documents, answer_query
import PyPDF2
import io
import os
import glob

# --- Page Configuration ---
st.set_page_config(
    page_title="Document Insight Engine",
    page_icon="📚",
    layout="centered"
)

# --- App Title ---
st.title("Multi-Document Insight Engine")
st.write(
    "Upload multiple documents and ask questions across all of them. "
    "The system retrieves relevant sections with source citations "
    "and supports cross-document comparison."
)

st.divider()

# --- Helper: Extract text from uploaded file ---
def extract_text(uploaded_file):
    """Extract text from a PDF or TXT file."""
    if uploaded_file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            pages = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            return "\n".join(pages)
        except Exception:
            return ""
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    return ""


# --- Helper: Load sample documents ---
def load_sample_documents():
    """Load .txt files from the sample_documents folder."""
    docs = []
    folder = "sample_documents"
    if os.path.exists(folder):
        for filepath in glob.glob(os.path.join(folder, "*.txt")):
            filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                docs.append({"name": filename, "content": content})
    return docs


# --- Document Upload ---
st.subheader("Step 1: Upload Documents")

uploaded_files = st.file_uploader(
    "Upload one or more documents (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

use_samples = st.checkbox(
    "Also include sample documents from the sample_documents folder",
    value=True
)

# --- Process Documents ---
process_button = st.button("Process Documents", type="primary")

if process_button:
    all_documents = []

    # Process uploaded files
    for uf in uploaded_files:
        text = extract_text(uf)
        if text.strip():
            all_documents.append({"name": uf.name, "content": text})

    # Add sample documents if selected
    if use_samples:
        sample_docs = load_sample_documents()
        all_documents.extend(sample_docs)

    if len(all_documents) == 0:
        st.warning(
            "No documents found. Please upload at least one file "
            "or enable sample documents."
        )
    else:
        with st.spinner(
            f"Processing {len(all_documents)} document(s). "
            "This may take a moment..."
        ):
            try:
                collection, stats = process_documents(all_documents)

                # Store in session state so it persists
                st.session_state["collection"] = collection
                st.session_state["stats"] = stats

                st.success(
                    f"Done! Processed {stats['total_documents']} documents "
                    f"into {stats['total_chunks']} searchable chunks."
                )

                # Show document list
                with st.expander("Documents indexed"):
                    for name in stats["document_names"]:
                        st.write(f"- {name}")

            except Exception as e:
                st.error(
                    "Something went wrong during processing. "
                    "Please check your API key and internet connection."
                )
                st.error(f"Error details: {e}")

st.divider()

# --- Query Section ---
st.subheader("Step 2: Ask a Question")

# Check if documents have been processed
if "collection" not in st.session_state:
    st.info("Please upload and process documents first (Step 1).")
    st.stop()

# Document filter dropdown
stats = st.session_state["stats"]
filter_options = ["All Documents"] + stats["document_names"]
source_filter = st.selectbox(
    "Search within",
    options=filter_options,
    index=0
)

# Query input
query = st.text_input(
    "Type your question here",
    placeholder="Example: What is the leave policy for new employees?"
)

search_button = st.button("Search and Answer", type="primary")

# --- Process Query ---
if search_button:
    if not query.strip():
        st.warning("Please type a question before searching.")
    else:
        collection = st.session_state["collection"]

        with st.spinner("Searching across documents..."):
            try:
                answer, results, query_type = answer_query(
                    collection, query, source_filter=source_filter
                )

                st.divider()

                # Query type badge
                if query_type == "comparison":
                    st.info("Cross-document comparison detected")

                # Answer
                st.subheader("Answer")
                st.markdown(answer)

                # Retrieved chunks with details
                if results:
                    st.divider()
                    st.subheader("Retrieved Sources")

                    for i, r in enumerate(results):
                        # Similarity score as a percentage (lower distance = better)
                        score = max(0, round((2 - r["distance"]) / 2 * 100, 1))

                        with st.expander(
                            f"Source: {r['source']} | "
                            f"Chunk {r['chunk_number']} | "
                            f"Relevance: {score}%"
                        ):
                            st.write(r["text"])
                            st.caption(
                                f"Distance: {r['distance']} | "
                                f"Relevance score: {score}%"
                            )

            except Exception as e:
                st.error(
                    "Something went wrong. "
                    "Please check your API key and internet connection."
                )
                st.error(f"Error details: {e}")
