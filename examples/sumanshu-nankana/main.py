from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from .routers import users, items, login
from .webapps import static_dir
from .webapps.routers import items as web_items
from .webapps.routers import users as web_users
from .webapps.routers import auth as web_auth
from config import settings


__version__ = '0.99.0'
desc = """
This is project description
"""

tags_metadata = [
    {"name": "user", "description": "This is user route"},
    {"name": "products", "description": "This is product route"},
]

# commented this line, because we have shifted to alembic migrations
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_TITLE,
    version=__version__,
    description=desc,
    openapi_tags=tags_metadata,
    contact={"name": "Sumanshu Nankana", "email": "sumanshunankana@gmail.com"},
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# we can pass the prefix argument as well
app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)
app.include_router(web_items.router)
app.include_router(web_users.router)
app.include_router(web_auth.router)
