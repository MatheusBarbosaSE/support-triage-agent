from fastapi import FastAPI, status
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file
genai.configure(api_key=os.getenv("AI_API_KEY"))

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
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Using an f-string to inject the ticket description directly into the prompt
    prompt = f"""
    Act as an expert IT support triage analyst.
    Analyze the following ticket description.
    Return strictly a JSON object with these exact keys: "category", "urgency", and "suggested_action".
    Do not include markdown formatting or any other text.
    
    Ticket Description: {ticket.description}
    """
    
    # We force the AI to return a clean JSON format
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )
    
    triage_data = json.loads(response.text)
    
    return TicketResponse(**triage_data)
