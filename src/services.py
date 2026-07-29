import os
import json
from sqlalchemy.orm import Session
from groq import Groq

from src import models
from src.schemas import TicketRequest, TicketResponse
from src.exceptions import handle_llm_api_error

# Initialize Groq client
client = Groq(api_key=os.getenv("AI_API_KEY"))

def analyze_ticket_with_llm(ticket: TicketRequest, db: Session) -> TicketResponse:
    """
    Sends the ticket description to the LLM, parses the structured data, 
    and persists the record in the database.
    """
    try:
        # 1. AI Processing
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
            model="llama-3.1-8b-instant",  
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content
        triage_data = json.loads(response_text)

        # 2. Database Persistence
        # Instantiate the SQLAlchemy model with the merged data
        new_ticket = models.Ticket(
            customer_name=ticket.customer_name,
            email=ticket.email,
            description=ticket.description,
            category=triage_data.get("category"),
            urgency=triage_data.get("urgency"),
            suggested_action=triage_data.get("suggested_action")
        )
        
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        
        # 3. Return the response to the user
        return TicketResponse(**triage_data)

    except Exception as e:
        # Passes any error caught to our centralized error handler
        handle_llm_api_error(e)
        