# app.py
# Streamlit interface for the AI-Powered Customer Support Assistant

import streamlit as st
from support_assistant import (
    load_knowledge_base,
    chunk_all_documents,
    build_vector_store,
    answer_query
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="💬",
    layout="centered"
)

# --- App Title and Description ---
st.title("AI-Powered Customer Support Assistant")
st.write(
    "Ask any question about our products, billing, or technical support. "
    "The assistant will find the best answer from our knowledge base."
)

st.divider()


# --- Load Knowledge Base (cached so it only runs once) ---
@st.cache_resource(show_spinner="Loading knowledge base...")
def initialize_system():
    """
    Load documents, chunk them, generate embeddings,
    and store in the vector database.
    This runs once and is cached for the session.
    """
    documents = load_knowledge_base("knowledge_base")
    chunks = chunk_all_documents(documents)
    collection = build_vector_store(chunks)
    doc_count = len(documents)
    chunk_count = len(chunks)
    return collection, doc_count, chunk_count


# Initialize the system
try:
    collection, doc_count, chunk_count = initialize_system()
    st.success(
        f"Knowledge base loaded: {doc_count} documents, "
        f"{chunk_count} chunks indexed."
    )
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(
        "Could not load the knowledge base. "
        "Please check your API key and the knowledge_base folder."
    )
    st.error(f"Error details: {e}")
    st.stop()

st.divider()

# --- Customer Query Input ---
st.subheader("How can we help you?")

query = st.text_input(
    "Type your question here",
    placeholder="Example: How do I return a product?"
)

ask_button = st.button("Get Answer", type="primary")

# --- Process Query ---
if ask_button:
    if not query.strip():
        st.warning("Please type a question before clicking Get Answer.")
    else:
        with st.spinner("Finding the best answer for you..."):
            try:
                response, confidence, sources = answer_query(collection, query)

                st.divider()

                # Confidence badge
                if confidence == "High":
                    st.success(f"Confidence: {confidence}")
                elif confidence == "Medium":
                    st.warning(f"Confidence: {confidence}")
                else:
                    st.error(f"Confidence: {confidence}")

                # Answer
                st.subheader("Answer")
                st.markdown(response)

                # Source references
                if sources:
                    unique_sources = list(set(sources))
                    source_text = ", ".join(unique_sources)
                    st.caption(f"Sources: {source_text}")

                # Escalation notice for low confidence
                if confidence == "Low":
                    st.divider()
                    st.info(
                        "Your question may require human assistance. "
                        "Please contact our support team at "
                        "support@example.com or call 1-800-555-0199."
                    )

            except Exception as e:
                st.error(
                    "Something went wrong. "
                    "Please check your API key and internet connection."
                )
                st.error(f"Error details: {e}")
