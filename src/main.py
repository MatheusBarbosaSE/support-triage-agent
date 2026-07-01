from fastapi import FastAPI, status

app = FastAPI()

@app.get("/api/v1/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Endpoint to verify if the server is healthy and running.
    """
    return {"status": "API is running"}
