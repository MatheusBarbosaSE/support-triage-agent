from pydantic import BaseModel

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
    