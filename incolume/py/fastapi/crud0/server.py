from fastapi import FastAPI
from config import settings
from incolume.py.fastapi.crud0 import __version__
from incolume.py.fastapi.crud0.routers import auth, user
from incolume.py.fastapi.crud0.db.persistence import create_db, recreate_db, populate_db


recreate_db()

app = FastAPI(
    title=settings.api_title,
    version=__version__,
    description=settings.api_description,
    openapi_tags=settings.api_openapi_tags,
    contact=settings.api_contact,
    docs_url=settings.api_docs_url,
    redoc_url=settings.api_redoc_url,
)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": settings.msg}


app.include_router(user.router, prefix="/users", tags=["Users"],)
app.include_router(auth.router, prefix="/auth", tags=["Auth"],)
