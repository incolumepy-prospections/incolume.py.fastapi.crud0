from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from incolume.py.fastapi.crud0.controllers.user import User
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0.schemas import UserIn, UserOut


router = APIRouter()

@router.post('/signin', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def user_register(user: UserIn, db_session: Session = Depends(get_db_session)):
    user = User(db_session=db_session).register(user=user)
    # return JSONResponse(content=user, status_code=status.HTTP_201_CREATED)
    return user
