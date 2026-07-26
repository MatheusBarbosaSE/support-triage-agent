import os
import json
from groq import Groq
from src.schemas import TicketRequest, TicketResponse
from src.exceptions import handle_llm_api_error

# Initialize Groq client
client = Groq(api_key=os.getenv("AI_API_KEY"))

def analyze_ticket_with_llm(ticket: TicketRequest) -> TicketResponse:
    """
    Sends the ticket description to the LLM and returns the parsed structured data.
    """
    try:
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
        
        return TicketResponse(**triage_data)

    except Exception as e:
        # Passes any error caught to our centralized error handler
        handle_llm_api_error(e)
        