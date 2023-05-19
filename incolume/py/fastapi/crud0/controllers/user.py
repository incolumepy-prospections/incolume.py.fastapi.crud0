"""Module User."""
import inspect
import logging
from inspect import stack
from datetime import datetime
from fastapi import status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.controllers.utils import QueryUser, Role
from incolume.py.fastapi.crud0.models import UserModel

crypt_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class User:
    """Class User."""

    def __init__(self, db_session: Session):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        self.db_session = db_session

    def __schema_user_to_user_in_db(
        self, user: schemas.UserLogin
    ) -> schemas.UserInDB:
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        hash = crypt_context.hash(user.password)
        del user.password
        new_user = schemas.UserInDB(**user.dict(), pw_hash=hash)
        logging.debug(f"{user=}>{new_user=}")
        return new_user

    def create(self, user: schemas.UserCreate) -> UserModel:
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        new_user: schemas.UserInDB = self.__schema_user_to_user_in_db(user)
        user_model = UserModel(**new_user.dict())
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            self.db_session.refresh(user_model)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User already exists. E-mail:'{new_user.email}' and/or username: '{new_user.username}' already registered.",
            )
        return user_model

    def all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        users = (
            self.db_session.query(UserModel).offset(skip).limit(limit).all()
        )
        return users

    def one(
        self, id_username_or_email: int | str, q: QueryUser = None
    ) -> UserModel:
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
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
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
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
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
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
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
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
        # new_user: schemas.UserInDB = schemas.UserInDB(
        #     **user.dict(), pw_hash=user_db.pw_hash)
        # logging.debug(f'{new_user=}')
        try:
            stmt = (
                update(UserModel).where(
                    UserModel.username == user.username
                ).values(
                    username=user.username,
                    full_name=user.full_name,
                    email=user.email,
                    update_at=datetime.utcnow(),
                )
            )
            self.db_session.execute(stmt)
            self.db_session.commit()
            self.db_session.refresh(user_db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"'{user.username}' "
                       f"or '{user.email}' already registered.",
            )
        return user_db

    def delete(self, param: int | str, q: QueryUser = None) -> UserModel:
        """Delete User."""
        q = q or QueryUser.ID
        try:
            match q:
                case QueryUser.USER_ID:
                    user = self.db_session.query(UserModel).where(
                        UserModel.id == int(param))
                case QueryUser.USER_EMAIL:
                    user = self.db_session.query(UserModel).where(
                        UserModel.email == param)
                case QueryUser.USERNAME:
                    user = self.db_session.query(UserModel).where(
                        UserModel.username == param)
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Query parameter not exists.",
                    )

        except ValueError as e:
            logging.error(e)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        user_db = user.first()
        logging.debug(f'{user_db=}')
        logging.debug(f"{user=}")
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        user.delete()
        self.db_session.commit()
        return user_db

    def toggle_active(self, param: int | str, q: QueryUser = None):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        user = self.one(param, q)
        user.is_active = not user.is_active
        user.update_at = datetime.utcnow()
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def promote_admin(self, param: int | str, q: QueryUser = None):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        user = self.one(param, q)
        user.update_at = datetime.utcnow()
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def set_role(
        self,
        param: int | str,
        q: QueryUser = None,
        roles: Role = None,
    ):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        logging.debug(f"--- {stack()[0][3]} ---")
        roles = roles or Role.USER
        q = q or QueryUser.ID
        logging.debug(f"{param=}, {q=}, {roles=}")
        user = self.one(param, q)
        user.roles = roles
        logging.debug(f'{roles=} > {user.roles=}')
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
