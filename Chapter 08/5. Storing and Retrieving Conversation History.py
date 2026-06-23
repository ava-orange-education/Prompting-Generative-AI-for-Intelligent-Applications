import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Load env vars
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# Store for message histories (in-memory for this example)
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Prompt template with memory slot
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Base chain (prompt -> LLM -> parser)
chain = prompt | llm | StrOutputParser()

# Wrap with message history
conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Simulate conversation with session ID
response1 = conversation.invoke(
    {"input": "My name is Jit."},
    config={"configurable": {"session_id": "user123"}}
)
print("AI:", response1)

response2 = conversation.invoke(
    {"input": "What is my name?"},
    config={"configurable": {"session_id": "user123"}}
)
print("AI:", response2)