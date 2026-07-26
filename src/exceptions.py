from fastapi import HTTPException, status
import groq
import json

def handle_llm_api_error(error: Exception):
    """
    Analyzes the exception raised by the LLM provider and raises the appropriate FastAPI HTTP exception.
    """
    if isinstance(error, groq.APIConnectionError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Error connecting to Groq API. Please check your network."
        )
    elif isinstance(error, groq.RateLimitError):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail="Rate limit exceeded. Please try again later."
        )
    elif isinstance(error, groq.APIStatusError):
        raise HTTPException(
            status_code=error.status_code, 
            detail=error.message
        )
    elif isinstance(error, json.JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="AI failed to return a valid JSON format."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An unexpected error occurred: {str(error)}"
        )
    