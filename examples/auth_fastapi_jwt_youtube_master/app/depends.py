from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .auth_user import UserUseCases
from .db.connection import Session

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_db_session():
    session: Session = Session()
    try:
        yield session
    finally:
        session.close()


def token_verifier(
    db_session: Session = Depends(get_db_session), token=Depends(oauth_scheme)
):
    uc = UserUseCases(db_session=db_session)
    uc.verify_token(access_token=token)
