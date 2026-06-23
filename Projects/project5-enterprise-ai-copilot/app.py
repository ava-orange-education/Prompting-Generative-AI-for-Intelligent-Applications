# app.py
# Streamlit chat interface for the Enterprise AI Copilot

import streamlit as st
from copilot_engine import ingest_documents, answer_query
from responsible_ai import run_safety_check

# --- Page Configuration ---
st.set_page_config(
    page_title="Enterprise AI Copilot",
    page_icon="🏢",
    layout="centered"
)

# --- App Title ---
st.title("Enterprise AI Copilot")
st.write(
    "Your internal knowledge assistant. Ask questions about company "
    "policies, processes, and guidelines. The copilot finds answers "
    "from company documents and remembers your conversation."
)

# --- Initialize Session State ---
if "collection" not in st.session_state:
    st.session_state["collection"] = None
    st.session_state["stats"] = None

if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Sidebar: Document Loading and Filters ---
with st.sidebar:
    st.header("Knowledge Base")

    if st.button("Load and Index Documents", type="primary"):
        with st.spinner("Processing company documents..."):
            try:
                collection, stats = ingest_documents("company_documents")
                st.session_state["collection"] = collection
                st.session_state["stats"] = stats

                # Clear conversation on re-index
                st.session_state["conversation_history"] = []
                st.session_state["messages"] = []

                st.success(
                    f"Indexed {stats['total_documents']} documents "
                    f"({stats['total_chunks']} chunks)"
                )
            except Exception as e:
                st.error(f"Failed to load documents: {e}")

    # Show indexed document details
    if st.session_state["stats"]:
        stats = st.session_state["stats"]
        st.divider()
        st.subheader("Indexed Documents")
        for doc in stats["documents"]:
            st.caption(f"📄 {doc['name']} ({doc['department']})")

        st.divider()

        # Department filter
        dept_options = ["All Departments"] + sorted(stats["departments"])
        department_filter = st.selectbox(
            "Filter by department",
            options=dept_options,
            index=0
        )
    else:
        department_filter = "All Departments"
        st.info("Click the button above to load documents.")

    # Clear conversation button
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state["conversation_history"] = []
        st.session_state["messages"] = []
        st.rerun()

# --- Main Chat Area ---

# Check if documents are loaded
if st.session_state["collection"] is None:
    st.info(
        "Please load company documents using the sidebar "
        "before asking questions."
    )
    st.stop()

# Display conversation history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show sources for assistant messages
        if message["role"] == "assistant" and "sources" in message:
            if message["sources"]:
                with st.expander("View sources"):
                    for s in message["sources"]:
                        score = max(0, round((2 - s["distance"]) / 2 * 100, 1))
                        st.caption(
                            f"📄 {s['source']} | "
                            f"{s['department']} | "
                            f"Chunk {s['chunk_number']} | "
                            f"Relevance: {score}%"
                        )

# Chat input
query = st.chat_input("Ask a question about company documents...")

if query:
    # Display user message
    st.session_state["messages"].append({
        "role": "user",
        "content": query
    })
    with st.chat_message("user"):
        st.markdown(query)

    # Responsible AI safety check
    is_safe, rejection_message = run_safety_check(query)

    if not is_safe:
        # Show rejection message
        st.session_state["messages"].append({
            "role": "assistant",
            "content": rejection_message,
            "sources": []
        })
        with st.chat_message("assistant"):
            st.markdown(rejection_message)
    else:
        # Process the query
        with st.chat_message("assistant"):
            with st.spinner("Searching company documents..."):
                try:
                    answer, results = answer_query(
                        collection=st.session_state["collection"],
                        query=query,
                        department_filter=department_filter,
                        conversation_history=st.session_state["conversation_history"]
                    )

                    st.markdown(answer)

                    # Show sources
                    if results:
                        with st.expander("View sources"):
                            for s in results:
                                score = max(0, round((2 - s["distance"]) / 2 * 100, 1))
                                st.caption(
                                    f"📄 {s['source']} | "
                                    f"{s['department']} | "
                                    f"Chunk {s['chunk_number']} | "
                                    f"Relevance: {score}%"
                                )

                    # Save to message history (for display)
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": answer,
                        "sources": results
                    })

                    # Save to conversation history (for memory)
                    st.session_state["conversation_history"].append({
                        "question": query,
                        "answer": answer
                    })

                except Exception as e:
                    error_msg = (
                        "Something went wrong. Please check your API key "
                        "and internet connection."
                    )
                    st.error(error_msg)
                    st.error(f"Error details: {e}")
