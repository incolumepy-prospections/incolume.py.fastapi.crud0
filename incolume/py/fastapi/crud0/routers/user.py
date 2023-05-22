"""Module endpoint for route user."""
import logging
from functools import singledispatch
from inspect import stack
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import Response, UJSONResponse
from sqlalchemy.orm import Session

from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.controllers.user import User
from incolume.py.fastapi.crud0.controllers.utils import (
    QueryUser,
    Role,
    Roles,
    ToggleBool,
)
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0.models import UserModel

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
    summary="Create an User",
)
def create_user(
    user: schemas.UserCreate, session: Session = Depends(get_db_session)
):
    """Create a new user."""
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
    """List all users."""
    return User(session).all(skip=skip, limit=limit)


@router.get(
    "/{id_username_or_email}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UserOut,
    summary="List an user by: id, email or username",
)
def get_user(
    id_username_or_email: int | str,
    q: QueryUser = Query(default=QueryUser.ID),
    db_session: Session = Depends(get_db_session),
):
    """Get a user by parameter."""
    user = User(db_session).one(id_username_or_email, q)
    logging.debug(user)
    return user


@router.post(
    "/toggle-active/{user_param}",
    summary="Toggle user status for is_active field",
    status_code=status.HTTP_202_ACCEPTED,
)
def toggle_active_user(
    user_param: int | str,
    q: QueryUser = Query(default=QueryUser.USER_ID),
    db_session: Session = Depends(get_db_session),
):
    """Active or Inactive a user."""
    user = User(db_session).toggle_active(user_param, q)
    return user


@router.put(
    "/{id_username_or_email}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UserOut,
    summary="Update data for user by id",
)
def update_user(
    user: schemas.UserUpdate,
    id_username_or_email: str,
    q: QueryUser = Query(default=QueryUser.USER_ID),
    db: Session = Depends(get_db_session),
):
    """Update a user."""
    user_updated = User(db).update(param=id_username_or_email, q=q, user=user)
    return user_updated


@router.delete(
    "/{param}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete an user by id",
)
def delete_user(
    param: str,
    q: QueryUser = QueryUser.ID,
    db_session: Session = Depends(get_db_session),
):
    """Delete a User."""
    user = User(db_session).delete(param=param, q=q)
    return user


@router.post(
    "/set-role/{param}",
    summary="Toggle role for actived users.",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=None,
)
def set_role_user(
    param: int | str,
    q: QueryUser = Query(
        title="Query type",
        description="Query type for param of user",
        default=QueryUser.USER_ID,
    ),
    roles: Roles = Roles.USER,
    db_session: Session = Depends(get_db_session),
):
    """Set roles for a user."""
    logging.debug(f"--- {stack()[0][3]} ---")
    user = User(db_session).set_role(param=param, roles=Role[roles], q=q)
    return user


@router.post(
    "/test-role/{user_param}",
    summary="Toggle role for actived users.",
    status_code=status.HTTP_202_ACCEPTED,
    # response_model=None,
    include_in_schema=False,
)
def test_role_user(
    user_param: str,
    q: QueryUser = QueryUser.ID,
    roles: Roles = Roles.USER,
    db: Session = Depends(get_db_session),
):
    """Return a user and roles."""
    user = User(db).one(user_param, q)
    return user, Role[roles]


@router.post("/classify", response_model=None, include_in_schema=False)
def classify(b: Roles = Roles.USER):
    """Return roles selected."""
    logging.debug(f"{b}")
    logging.debug(f"{Role[b.upper()]}")
    return b, Role[b.upper()]
