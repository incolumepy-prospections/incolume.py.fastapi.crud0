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
    
    def __user_in_to_user_in_db(self, user: UserIn) -> UserInDB:
        hash = crypt_context.hash(user.password)
        del user.password
        new_user = UserInDB(**user.dict(), pw_hash=hash)
        logging.debug(f'{usar=}>{new_user=}')
        return new_user
        
    def create(self, user: UserIn) -> UserModel:
        new_user: UserInDB = self.__user_in_to_user_in_db(user)
        user_model = UserModel(**new_user.dict())
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            self.db_session.refresh(user_model)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists.')
        return user_model
        
    def all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        users = self.db_session.query(UserModel).offset(skip).limit(limit).all()
        return users

    def one(self, user_id: int) -> UserModel:
        user = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

        logging.debug(f'{user=}')
        return user
    
    def by_username(self, username: str) -> UserModel:
        user = self.db_session.query(UserModel).filter(UserModel.username == username).first()
        logging.debug(f'{user=}')
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
        return user

    def by_email(self, email: str) -> UserModel:
        user = self.db_session.query(UserModel).filter(UserModel.email == email).first()
        logging.debug(f'{user=}')
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
        return user
    
    def update(self, user_id: int, user: UserIn) -> UserModel:
        logging.debug(f'{user_id=}')
        logging.debug(f'{user=}')
        user_db = self.one(user_id)
        logging.debug(f'{user_db=}')
        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
        #TODO: Não permitir que id seja alterado.
        new_user: UserInDB = self.__user_in_to_user_in_db(user)
        stmt = update(UserModel).where(user_db.id == user_id).values(**new_user)
        self.db_session.execute(stmt)
        self.db_session.commit()
        self.db_session.refresh(user_db)
        return user_db
    
    def delete(self, user_id: int) -> UserModel:
        user = self.db_session.query(UserModel).where(UserModel.id == user_id)
        logging.debug(f'{user=}')
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
        
        user.delete()
        self.db_session.commit()
        return user

