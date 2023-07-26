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

# Define the function_descriptions outside of the scope of the routes
function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email"
                },
                "product": {
                    "type": "string",
                    "description": "Try to identify which product the client is interested in, if any"
                },
                "amount":{
                    "type": "string",
                    "description": "Try to identify the amount of products the client wants to purchase, if any"
                },
                "category": {
                    "type": "string",
                    "description": "Try to categorise this email into categories like those: 1. Sales 2. customer support; 3. consulting; 4. partnership; etc."
                },
                "nextStep":{
                    "type": "string",
                    "description": "What is the suggested next step to move this forward?"
                },
                "priority": {
                    "type": "string",
                    "description": "Try to give a priority score to this email based on how likely this email will leads to a good business opportunity, from 0 to 10; 10 most important"
                },
            },
            "required": ["companyName", "amount", "product", "priority", "category", "nextStep"]
        }
    }
]

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

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions=function_descriptions,
        function_call="auto"
    )

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
