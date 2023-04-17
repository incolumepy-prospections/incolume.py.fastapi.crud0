from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from incolume.py.fastapi.crud0.controllers.user import User
from incolume.py.fastapi.crud0.controllers.auth import Auth
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0.schemas import UserIn, UserOut


router = APIRouter(prefix='/auth')


@router.post('/login')
def user_login(login_request_form: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db_session)):
    user_ = User(db_session)
    user_in = UserIn(**login_request_form)
    # return JSONResponse(content=user, status_code=status.HTTP_201_CREATED)
    return user
