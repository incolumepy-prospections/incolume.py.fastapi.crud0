import logging
import json
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import status
from fastapi.exceptions import HTTPException

from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.controllers.utils import QueryUser, Role
from incolume.py.fastapi.crud0.models import UserModel

crypt_context = CryptContext(schemes=["sha256_crypt"])


class User:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def __schema_user_to_user_in_db(
        self, user: schemas.UserLogin
    ) -> schemas.UserInDB:
        hash = crypt_context.hash(user.password)
        del user.password
        new_user = schemas.UserInDB(**user.dict(), pw_hash=hash)
        logging.debug(f"{user=}>{new_user=}")
        return new_user

    def create(self, user: schemas.UserCreate) -> UserModel:
        new_user: schemas.UserInDB = self.__schema_user_to_user_in_db(user)
        user_model = UserModel(**new_user.dict())
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            self.db_session.refresh(user_model)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists.",
            )
        return user_model

    def all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        users = (
            self.db_session.query(UserModel).offset(skip).limit(limit).all()
        )
        return users

    def one(
        self, id_username_or_email: int | str, q: QueryUser = None
    ) -> UserModel:
        q = q or QueryUser.ID
        logging.debug(f"{id_username_or_email=}, {q=}")
        try:
            match q:
                case QueryUser.USER_ID:
                    logging.debug("--- id ---")
                    user = self.by_id(int(id_username_or_email))
                case QueryUser.EMAIL:
                    logging.debug("--- email ---")
                    user = self.by_email(id_username_or_email)
                case QueryUser.USERNAME:
                    logging.debug("--- username ---")
                    user = self.by_username(id_username_or_email)
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Query parameter not exists.",
                    )
            logging.debug(user)
            return user
        except ValueError as e:
            logging.error(e)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

    def by_id(self, user_id: int) -> UserModel:
        user = (
            self.db_session.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        logging.debug(f"{user=}")
        return user

    def by_username(self, username: str) -> UserModel:
        user = (
            self.db_session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )
        logging.debug(f"{user=}")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        return user

    def by_email(self, email: str) -> UserModel:
        user = (
            self.db_session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )
        logging.debug(f"{user=}")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        return user

    def update(
        self,
        user: schemas.UserUpdate,
        param: int | str,
        q: QueryUser = None
    ) -> UserModel:
        """Update Users."""
        logging.debug('--- User.update ---')
        
        q = q or QueryUser.USER_ID
        logging.debug(f"{param=}, {q=}, {user.dict()=}")

        user_db = self.one(param, q)
        logging.debug(f"{user_db.__dict__=}")

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        # TODO: Não permitir que id seja alterado.
        # TODO: Não permitir que senha seja alterada.
        new_user: schemas.UserInDB = schemas.UserInDB(
            **user.dict(), pw_hash=user_db.pw_hash)
        logging.debug(f'{new_user=}')

        stmt = (
            update(UserModel).where(
                user_db.username == user.username).values(**new_user)
        )
        self.db_session.execute(stmt)
        self.db_session.commit()
        self.db_session.refresh(user_db)
        return user_db

    def delete(self, user_id: int) -> UserModel:
        user = self.db_session.query(UserModel).where(UserModel.id == user_id)
        user_db = user.first()
        print(user_db)
        logging.debug(f"{user=}")
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        user.delete()
        self.db_session.commit()
        return user_db

    def toggle_active(self, param: int | str, q: QueryUser = None):
        user = self.one(param, q)
        user.is_active = not user.is_active
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def promote_admin(self, param: int | str, q: QueryUser = None):
        user = self.one(param, q)
        user.is_admin = not user.is_admin
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def set_role(
        self,
        param: int | str,
        roles: list[Role] = None,
        q: QueryUser = None,
    ):
        roles = roles or [Role.USER]
        logging.debug(f"{param=}, {q=}, {roles=}")
        logging.debug("--- ** ---")
        user = self.one(param, q)
        uroles: list = json.loads(user.roles)
        user.roles = uroles.extend(roles)
        logging.debug(roles)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
