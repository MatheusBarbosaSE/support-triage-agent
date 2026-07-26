from fastapi import FastAPI, status
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

# Initialize Groq client using the requested environment variable
client = Groq(api_key=os.getenv("AI_API_KEY"))

app = FastAPI()

@app.get("/api/v1/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Endpoint to verify if the server is healthy and running.
    """
    return {"status": "API is running"}

class TicketRequest(BaseModel):
    """
    Model representing a ticket request.
    """
    customer_name: str
    email: str
    description: str

class TicketResponse(BaseModel):
    """
    Model representing a ticket response.
    """
    category: str
    urgency: str
    suggested_action: str

@app.post("/api/v1/triage", status_code=status.HTTP_200_OK)
async def triage_ticket(ticket: TicketRequest):
    """
    Endpoint to process a ticket and return an AI-based triage.
    """
    
    # Groq uses standard Chat Completion structure (System and User messages)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Act as an expert IT support triage analyst. Analyze the ticket and return strictly a JSON object with these exact keys: 'category', 'urgency', and 'suggested_action'. Do not include markdown formatting or any conversational text."
            },
            {
                "role": "user",
                "content": f"Ticket Description: {ticket.description}"
            }
        ],
        model="llama-3.1-8b-instant",  # Updated to the current active Meta Llama 3.1 model
        response_format={"type": "json_object"}  # Forcing the AI to return a clean JSON format
    )
    
    # Extracting the text from the Groq response object
    response_text = chat_completion.choices[0].message.content
    
    # Converting the AI string into a Python Dictionary
    triage_data = json.loads(response_text)
    
    # Returning and validating through our Pydantic model
    return TicketResponse(**triage_data)