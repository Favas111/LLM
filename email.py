import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import json

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
# ... (your other code)

email = """
Dear Jason 
I hope this message finds you well. I'm Shirley from Gucci;

I'm looking to purchase some company T-shirt for my team, we are a team of 100k people, and we want to get 2 t-shirt per personl

Please let me know the price and timeline you can work with;

Looking forward

Shirley Lou
"""

prompt = f"Please extract key information from this email: {email} "
message = [{"role": "user", "content": prompt}]

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=message,
    functions=function_descriptions,
    function_call="auto"
)

print(response)

response_message = response["choices"][0]["message"]
function_arguments_str = response_message["function_call"]["arguments"]
function_arguments = json.loads(function_arguments_str)
print(function_arguments)

class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content} "

    messages = [{"role": "user", "content": query}]

    response_message = response["choices"][0]["message"]
    function_arguments_str = response_message["function_call"]["arguments"]
    function_arguments = json.loads(function_arguments_str)

    companyName = function_arguments.get("companyName")
    priority = function_arguments.get("priority")
    product = function_arguments.get("product")
    amount = function_arguments.get("amount")
    category = function_arguments.get("category")
    nextStep = function_arguments.get("nextStep")

    return {
        "companyName": companyName,
        "product": product,
        "amount": amount,
        "priority": priority,
        "category": category,
        "nextStep": nextStep
    }
