from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

def ingredient_available(item, ingredients):
    return item in ingredients

tools = [
    {
        "type": "function",
        "function": {
            "name": "ingredient_available",
            "description": "Check if an ingredient is available",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"}
                },
                "required": ["item"]
            }
        }
    }
]

ingredients = ["tomato", "rice", "potato"]

messages = [
    {
        "role": "user",
        "content": f"""You are an AI chef. Ingredients available: {ingredients}. 
        
        Before deciding what to cook:
        - You MUST check whether rice is available using the ingredient_available tool.
        - Do not assume availability.
        - Call the tool first, then decide the next step.
        
        """
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

if message.tool_calls:
    print("Model requested a tool call")
else:
    print(message.content)
print('-------------------------')

message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name
    tool_args = tool_call.function.arguments
else:
    print("No tool call requested by the model.")
    print(message.content)
    exit()

if tool_name == "ingredient_available":
    item = eval(tool_args)["item"]
    result = ingredient_available(item, ingredients)

messages.append(response.choices[0].message)

messages.append(
    {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    }
)

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(final_response.choices[0].message.content)