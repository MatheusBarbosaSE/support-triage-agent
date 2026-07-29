from sqlalchemy import Column, Integer, String
from src.database import Base

class Ticket(Base):
    """
    SQLAlchemy model representing the 'tickets' table in the database.
    Stores both the user request and the AI-generated triage response.
    """
    
    __tablename__ = "tickets"

    # Primary Key: Unique identifier for each ticket
    id = Column(Integer, primary_key=True, index=True)
    
    # Data from the user (TicketRequest)
    customer_name = Column(String, index=True)
    email = Column(String, index=True)
    description = Column(String)
    
    # Data from the AI (TicketResponse)
    category = Column(String, index=True)
    urgency = Column(String, index=True)
    suggested_action = Column(String)
    