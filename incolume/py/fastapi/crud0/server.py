from fastapi import FastAPI
from config import settings


app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return {"message": settings.msg}
