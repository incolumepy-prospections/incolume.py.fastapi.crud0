"""Server module."""
from fastapi import FastAPI


app = FastAPI(title='sketch')


@app.get("/")
async def root(msg: str = ""):
    """Endpoint for root."""
    msg = msg or "Hello world"
    return {"greeting": msg}
