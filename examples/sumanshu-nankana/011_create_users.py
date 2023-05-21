from fastapi import FastAPI, Depends
from config import settings
from .database import engine, get_db
from .models import Base, User
from .schemas import UserCreate
from .hashing import Hasher
from sqlalchemy.orm import Session
from .routers import users

__version__ = '1.0.0'
desc = f"""
# Description for {settings.API_TITLE}
This is **project** description
"""

tags_metadata = [
    {"name": "user", "description": "This is user route"},
    {"name": "products", "description": "This is product route"},
]


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_TITLE,
    version=__version__,
    description=desc,
    openapi_tags=tags_metadata,
    contact={"name": "Sumanshu Nankana", "email": "sumanshunankana@gmail.com"},
    redoc_url=None,
)

app.include_router(users.router)
