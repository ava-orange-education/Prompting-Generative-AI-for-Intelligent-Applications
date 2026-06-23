from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Load API key
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create a simple calculator tool
@tool
def calculator(expression: str) -> str:
    """Useful for doing math calculations. Input should be a valid Python math expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Bind tools directly to the LLM
llm_with_tools = llm.bind_tools([calculator])

# Get initial response
question = "What is 15% of 360?"
response = llm_with_tools.invoke(question)

# Check if tool was called
if response.tool_calls:
    tool_call = response.tool_calls[0]
    print(f"Tool called: {tool_call['name']}")
    print(f"Arguments: {tool_call['args']}")
    
    # Execute the tool
    tool_result = calculator.invoke(tool_call['args'])
    print(f"Tool result: {tool_result}")
    
    # Send result back to LLM for final answer
    
    
    messages = [
        HumanMessage(content=question),
        response,  # AI's decision to use tool
        ToolMessage(content=str(tool_result), tool_call_id=tool_call['id'])
    ]
    
    final_response = llm.invoke(messages)
    print(f"\nFinal Answer: {final_response.content}")
else:
    print(response.content)