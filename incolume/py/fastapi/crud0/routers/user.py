from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.controllers.user import User

router = APIRouter(prefix='/users')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def signin(user: schemas.UserIn, session: Session = Depends(get_db_session)):
    new_user = User(session).create(user)
    return new_user


@router.get('/', status_code=status.HTTP_202_ACCEPTED)
def list_users(skip:int = 0, limit=10, session: Session = Depends(get_db_session)):
    return User(session).all(skip=skip, limit=limit)


@router.get('/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db_session)):
    user = User(db).one(user_id)
    return user

@router.get('/{username_or_email}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def get_user_by_username_or_email(username_or_email: str, db: Session = Depends(get_db_session)):
    try:
        user = User(db).by_username(username_or_email)
    except Exception as e:
        print(e)
        user = User(db).by_email(username_or_email)
    return user


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, db: Session = Depends(get_db_session)):
    user = User(db).update(user_id)
    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    user = User(db).delete(user_id)
    return user
