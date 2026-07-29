from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.schemas import TicketRequest, TicketResponse
from src.services import analyze_ticket_with_llm
from src.database import get_db

# Creating the router instance with prefix and tags for Swagger UI
router = APIRouter(prefix="/api/v1", tags=["Triage"])

# Notice the dependency injection here in the parameters: db: Session = Depends(get_db)
@router.post("/triage", status_code=status.HTTP_200_OK, response_model=TicketResponse)
async def triage_ticket(ticket: TicketRequest, db: Session = Depends(get_db)):
    """
    Endpoint to process a ticket and return an AI-based triage.
    """
    # Now we pass both the ticket and the database session to the service
    return analyze_ticket_with_llm(ticket, db)
