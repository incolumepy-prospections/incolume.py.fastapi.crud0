from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from incolume.py.fastapi.crud0 import __version__
from incolume.py.fastapi.crud0.controllers.auth import token_verifier
from incolume.py.fastapi.crud0.db.persistence import (
    create_admin,
    create_db,
    populate_db,
    recreate_db,
)
from incolume.py.fastapi.crud0.routers import auth, auth_otp, items, user

recreate_db()
create_admin()


app = FastAPI(
    title=settings.api_title,
    version=__version__,
    description=settings.api_description,
    openapi_tags=settings.api_openapi_tags,
    contact=settings.api_contact,
    docs_url=settings.api_docs_url,
    redoc_url=settings.api_redoc_url,
    license_info=settings.api_license,
)

static = Path(__file__).parents[4] / "static"

app.mount("/static", StaticFiles(directory=static), name="static")


@app.get("/", include_in_schema=False)
async def root():
    return {"message": settings.msg}


@app.get(
    "/doc",
    response_class=RedirectResponse,
    status_code=308,
    include_in_schema=False,
)
async def redirect_pydantic():
    return "/docs"


@app.get(
    "/favicon.ico",
    response_class=RedirectResponse,
    status_code=307,
    include_in_schema=False,
)
async def redirect_pydantic():
    return "/static/img/favicon.png"


app.include_router(
    items.router,
    prefix="/items",
    tags=["Items"],
    dependencies=[
        Depends(token_verifier),
    ],
)
app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
)
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    auth_otp.router,
    prefix="/auth/otp",
    tags=["Auth OTP"],
)
