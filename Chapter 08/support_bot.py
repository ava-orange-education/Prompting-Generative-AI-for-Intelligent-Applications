import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import SystemMessage

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Model
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
    temperature=0
)

# ---------------------------
# System context (your initial instruction)
# ---------------------------
system_context = """
You are a helpful customer support assistant for a tech company. 
Be friendly, clear, and professional. Remember details the user shares.
"""

# ---------------------------
# Message history store
# ---------------------------
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        # Initialize with system message
        store[session_id] = ChatMessageHistory()
        store[session_id].add_message(SystemMessage(content=system_context))
    return store[session_id]

# ---------------------------
# Modern prompt with memory placeholder
# ---------------------------
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

parser = StrOutputParser()

# ---------------------------
# Build a full conversational chain
# ---------------------------
chain = prompt | llm | parser

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# ---------------------------
# Chat Loop
# ---------------------------
print("Customer Support Bot (LangChain 1.x)")
print("Type 'quit' to exit.\n")

session_id = "support_session_001"  # You can make this dynamic per user

while True:
    user_input = input("Customer: ")

    if user_input.lower() == "quit":
        print("Support: Thank you for contacting support!")
        break

    response = conversation.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"Support: {response}\n")