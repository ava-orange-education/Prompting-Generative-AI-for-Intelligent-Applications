# app.py
# Streamlit interface for the Multi-Agent Research Assistant

import streamlit as st
from research_agents import (
    run_research_agent,
    run_analysis_agent,
    run_report_writer_agent
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="centered"
)

# --- App Title ---
st.title("Multi-Agent Research Assistant")
st.write(
    "Enter a research topic and watch three AI agents collaborate "
    "to produce a structured report. Each agent has a specific role "
    "and passes its output to the next."
)

st.divider()

# --- Topic Input ---
st.subheader("Enter Your Research Topic")

topic = st.text_input(
    "What topic would you like to research?",
    placeholder="Example: The impact of electric vehicles on the global auto industry"
)

st.caption(
    "Tip: Specific topics produce better results. "
    "\"AI in healthcare\" is good, but \"How AI is improving early cancer detection\" is better."
)

generate_button = st.button("Generate Research Report", type="primary")

st.divider()

# --- Run Pipeline ---
if generate_button:
    if not topic.strip():
        st.warning("Please enter a research topic before generating.")
    elif len(topic.split()) < 3:
        st.warning(
            "Your topic seems very short. "
            "Try adding more detail for better results."
        )
    else:
        total_tokens = 0

        # --- Agent 1: Research ---
        st.subheader("Agent 1: Research Agent")
        st.caption("Role: Gather information and identify key subtopics")

        with st.spinner("Research Agent is working..."):
            try:
                research_output, research_tokens = run_research_agent(topic)
                total_tokens += research_tokens

                st.success(
                    f"Research complete. ({research_tokens} tokens used)"
                )
                with st.expander("View Research Agent output"):
                    st.markdown(research_output)

            except Exception as e:
                st.error(f"Research Agent failed: {e}")
                st.stop()

        # --- Agent 2: Analysis ---
        st.subheader("Agent 2: Analysis Agent")
        st.caption("Role: Evaluate research and identify patterns, risks, and opportunities")

        with st.spinner("Analysis Agent is working..."):
            try:
                analysis_output, analysis_tokens = run_analysis_agent(
                    topic, research_output
                )
                total_tokens += analysis_tokens

                st.success(
                    f"Analysis complete. ({analysis_tokens} tokens used)"
                )
                with st.expander("View Analysis Agent output"):
                    st.markdown(analysis_output)

            except Exception as e:
                st.error(f"Analysis Agent failed: {e}")
                st.stop()

        # --- Agent 3: Report Writer ---
        st.subheader("Agent 3: Report Writer Agent")
        st.caption("Role: Structure everything into a professional report")

        with st.spinner("Report Writer Agent is working..."):
            try:
                report_output, report_tokens = run_report_writer_agent(
                    topic, research_output, analysis_output
                )
                total_tokens += report_tokens

                st.success(
                    f"Report complete. ({report_tokens} tokens used)"
                )

            except Exception as e:
                st.error(f"Report Writer Agent failed: {e}")
                st.stop()

        # --- Final Report ---
        st.divider()
        st.subheader("Final Research Report")
        st.markdown(report_output)

        # --- Token Usage Summary ---
        st.divider()
        st.caption(
            f"Total tokens used: {total_tokens} | "
            f"Research: {research_tokens} | "
            f"Analysis: {analysis_tokens} | "
            f"Report: {report_tokens}"
        )
