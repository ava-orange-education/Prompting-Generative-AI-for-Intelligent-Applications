from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

st.title("AI Contract Helper")
st.write("Upload a contract and get a summary with key points.")
uploaded_file = st.file_uploader("Upload a contract file", type=["txt"])

if uploaded_file is not None:
    contract_text = uploaded_file.read().decode("utf-8")
    st.markdown("### Preview of the document")
    st.write(contract_text[:1000])

analyze = st.button("Summarise and extract key points")

if analyze:
    if uploaded_file is None:
        st.warning("Please upload a contract file first.")
    else:
        with st.spinner("Analyzing the contract..."):
            prompt = f"""
            You are a helpful assistant that reads contracts.
            Summarise the following contract in a short paragraph.
            Then list the most important points and obligations as bullet points.
            
            Contract text:
            {contract_text}
            """

            response = client.chat.completions.create(model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}])

            ai_output = response.choices[0].message.content

            st.success("Analysis complete.")
            st.markdown("### Summary and Key Points")
            st.write(ai_output)
follow_up = st.text_input("Ask a follow up question about this contract")
if st.button("Ask follow up"):
    with st.spinner("Thinking..."):
        follow_prompt = f"""
        You already read the following contract:

        {contract_text}

        Now answer this question clearly:
        {follow_up}
        """

        follow_response = client.chat.completions.create(model="gpt-4o-mini",
                messages=[{"role": "user", "content": follow_prompt}])

        st.markdown("### Follow up answer")
        st.write(follow_response.choices[0].message.content)




