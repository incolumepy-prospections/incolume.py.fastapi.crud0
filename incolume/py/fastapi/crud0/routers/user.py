import logging
from typing import Any

from fastapi import APIRouter, Depends, status, Query
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from incolume.py.fastapi.crud0.controllers.utils import QueryUser, Role
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.controllers.user import User
from incolume.py.fastapi.crud0.models import UserModel
from functools import singledispatch

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
    summary="Create an User",
)
def signin(
    user: schemas.UserCreate, session: Session = Depends(get_db_session)
):
    new_user: UserModel = User(session).create(user)
    return new_user


@router.get(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=list[schemas.UserOut],
    summary="List all users",
)
def list_users(
    skip: int = 0, limit=10, session: Session = Depends(get_db_session)
):
    return User(session).all(skip=skip, limit=limit)


# @router.get('/{user_id: int}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut, summary="List an user by id")
# def get_user(user_id: int, db: Session = Depends(get_db_session)):
#     user = User(db).one(user_id)
#     return user

# @router.get('/{username_or_email: str}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut, summary="List an user by username or email")
# def get_user_by_username_or_email(username_or_email: str, db: Session = Depends(get_db_session)):
#     user = User(db).by_email(username_or_email) or User(db).by_username(username_or_email)
#     return user


# @router.get('/{id_username_or_email}', status_code=status.HTTP_202_ACCEPTED)
# def get_user(id_username_or_email, db: Session = Depends(get_db_session)):
#     print(f'value: {id_username_or_email}, type: {type(id_username_or_email)}')
#
#     if isinstance(id_username_or_email, str):
#         try:
#             user = User(db).by_username(id_username_or_email)
#         except Exception as e:
#             print(e)
#             user = User(db).by_email(id_username_or_email)
#     else:
#         user = User(db).one(id_username_or_email)
#
#     return user


@router.get(
    "/{id_username_or_email}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UserOut,
    summary="List an user by: id, email or username",
)
def get_user(
    id_username_or_email: int | str,
    q: QueryUser = Query(default=QueryUser.ID),
    db: Session = Depends(get_db_session),
):
    user = User(db).one(id_username_or_email, q)
    logging.debug(user)
    return user


@router.post(
    "/toggle_active/{user_param}",
    summary="Toggle user status for is_active field",
    status_code=status.HTTP_202_ACCEPTED,
)
def toggle_active_user(
    user_param: int | str,
    q: QueryUser = Query(default=QueryUser.USER_ID),
    db: Session = Depends(get_db_session),
):
    user = User(db).toggle_active(user_param, q)
    return user


@router.put(
    "/{id_username_or_email}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update data for user by id",
)
def update_user(
    user: schemas.UserUpdate,
    id_username_or_email: str,
    q: QueryUser = Query(default=QueryUser.USER_ID),
    db: Session = Depends(get_db_session),
):
    user_updated = User(db).update(param=id_username_or_email, q=q, user=user)
    return user_updated


@router.delete(
    "/{param}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete an user by id",
)
def delete_user(param: str, q: QueryUser = QueryUser.ID, db: Session = Depends(get_db_session)):
    user = User(db).delete(param=param, q=q)
    return user


@router.post(
    "/set-role/{user_param}",
    summary="Toggle user status for is_active field",
    status_code=status.HTTP_202_ACCEPTED,
)
def set_role_user(
    user_param: int | str,
    roles: list[Role] = Query(default=[Role.USER]),
    q: QueryUser = Query(default=QueryUser.USER_ID),
    db: Session = Depends(get_db_session),
):
    user = User(db).set_role(user_param, roles=roles, q=q)
    return user
