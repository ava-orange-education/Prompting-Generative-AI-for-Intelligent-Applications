from langchain_core.tools import Tool
from dotenv import load_dotenv
import os

load_dotenv()

def discount(price, rate):
    return price - (price * rate / 100)

discount_tool = Tool(
    name="Discount Calculator",
    func=lambda x: discount(*map(float, x.split(","))),
    description="Calculates discounted price given amount and rate. Format: 'price,rate'"
)

# Test the tool directly
print(discount_tool.invoke({"input": "100,10"}))