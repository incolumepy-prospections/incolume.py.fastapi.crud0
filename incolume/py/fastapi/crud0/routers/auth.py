import logging

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from incolume.py.fastapi.crud0.controllers.auth import Auth, token_verifier
from incolume.py.fastapi.crud0.controllers.user import User
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0.schemas import UserLogin, UserOut

router = APIRouter(prefix="")


@router.get(
    "/{whoami}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserOut,
    summary="Show corrent user logged.",
)
def whoami(
    db: Session = Depends(get_db_session),
):
    user = User(db).one(10)
    logging.debug(user)
    return user


@router.post("/login")
def user_login(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    user_in = UserLogin(
        username=login_request_form.username,
        password=login_request_form.password,
    )
    user_auth = Auth(db_session).login(user_in)
    # return JSONResponse(content=user, status_code=status.HTTP_201_CREATED)
    return user_auth


@router.get("/check", status_code=202)
def check_token(token_verified=Depends(token_verifier)):
    return {"details": True}


@router.post("/new-token-jwt")
def get_new_token(
    request_form: OAuth2PasswordRequestForm = Depends(),
    token_verified=Depends(token_verifier),
    db_session: Session = Depends(get_db_session),
):
    pass
