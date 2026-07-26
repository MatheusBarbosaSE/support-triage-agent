from fastapi import FastAPI, status
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

from src.routers import triage

app = FastAPI(title="Support Triage Agent API")

# Registering the domain routers
app.include_router(triage.router)

@app.get("/api/v1/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    """
    Endpoint to verify if the server is healthy and running.
    """
    return {"status": "API is running"}
