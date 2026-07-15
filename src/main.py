from fastapi import FastAPI, status
from pydantic import BaseModel

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
    Endpoint to process a ticket and return an AI-based triage (Mocked).
    """
    triage_response = TicketResponse(
        category="Technical",
        urgency="High",
        suggested_action="Please address this issue immediately."
    )
    return triage_response
