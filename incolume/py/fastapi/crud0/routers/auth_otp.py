"""Router Auth OTP."""
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from incolume.py.fastapi.crud0.controllers.auth import AuthOTP
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0.schemas import UserLogin

router = APIRouter(prefix="")


@router.get("/favicon")
async def get_favicon():
    """Favicon route."""
    image: Path = (
        Path(__file__).parents[5].joinpath("static", "img", "favicon.png")
    )
    logging.debug(f"{image=}")
    return FileResponse(image.as_posix(), media_type="image/png")


@router.post("/login")
def user_login(
    username: str = Form(...),
    password: str = Form(...),
    db_session: Session = Depends(get_db_session),
):
    """Login route."""
    user_in = UserLogin(username=username, password=password)
    user_auth = AuthOTP(db_session).login(user_in)
    return user_auth


# @router.get('/check')
# def check_token(token_verified = Depends(token_verifier)):
#     """Checking."""
#     return {'details': True}
