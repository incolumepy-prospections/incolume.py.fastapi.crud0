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
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists.')
        return user_model
        
    def update(self, user_id: int) -> UserModel:
        pass

    def delete(self) -> UserModel:
        pass

    def all(self) -> list[UserModel]:
        users = self.db_session.query(UserModel).all()
        return users

    def one(self, user_id: int) -> UserModel:
        stmt = select(UserModel).filter_by(id=user_id)
        user = self.db.execute(stmt).one()
        return user
