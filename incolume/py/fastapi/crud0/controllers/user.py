import logging
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import status
from fastapi.exceptions import HTTPException

from incolume.py.fastapi.crud0.models import UserModel
from incolume.py.fastapi.crud0.schemas import UserIn, UserInDB


crypt_context = CryptContext(schemes=['sha256_crypt'])


class User:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: UserIn) -> UserModel:
        hash=crypt_context.hash(user.password)
        del user.password
        new_user = UserInDB(**user.dict(), pw_hash=hash)
        user_model = UserModel(**new_user.dict())
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            self.db_session.refresh(user_model)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists.')
        return user_model
        
    def update(self, user_id: int, user: UserIn) -> UserModel:
        user_db = self.one(user_id)
        stmt = update(UserModel).where(user_db.id == user_id).values(**user)
        self.db_session.execute(stmt)
        self.db_session.commit()
        self.db_session.refresh(user_db)
        return user_db

    def delete(self, user_id: int) -> UserModel:
        user = self.one(user_id)
        stmt = delete(user)
        self.db_session.execute(stmt)
        return user

    def all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        users = self.db_session.query(UserModel).offset(skip).limit(limit).all()
        return users

    def one(self, user_id: int) -> UserModel:
        stmt = select(UserModel).filter_by(id=user_id)
        user = self.db_session.execute(stmt).first()
        logging.debug(f'{user=}')
        return user
    
    def by_username(self, username: str) -> UserModel:
        return self.db_session.query(UserModel).filter(UserModel.username == username).first()

    def by_email(self, email: str) -> UserModel:
        return self.db_session.query(UserModel).filter(UserModel.email == email).first()
