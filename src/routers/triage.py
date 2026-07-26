from fastapi import APIRouter, status
from src.schemas import TicketRequest, TicketResponse
from src.services import analyze_ticket_with_llm

# Creating the router instance with prefix and tags for Swagger UI
router = APIRouter(prefix="/api/v1", tags=["Triage"])

@router.post("/triage", status_code=status.HTTP_200_OK, response_model=TicketResponse)
async def triage_ticket(ticket: TicketRequest):
    """
    Endpoint to process a ticket and return an AI-based triage.
    """
    return analyze_ticket_with_llm(ticket)
