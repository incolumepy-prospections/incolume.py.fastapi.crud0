"""Server module."""
from fastapi import FastAPI

app = FastAPI(title="draft")


@app.get("/")
async def root(msg: str = ""):
    """Endpoint for root."""
    msg = msg or "Hello world"
    return {"greeting": msg}