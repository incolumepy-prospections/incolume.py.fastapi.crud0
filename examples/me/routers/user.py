"""Routers for user."""
import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException

from incolume.py.fastapi.crud2.data_base.connections import db
from incolume.py.fastapi.crud2.schemas import UpdateUser, User

router = APIRouter(prefix="/user")


@router.post("/", tags=["Users"], status_code=201)
async def create_user(user: User):
    """Create User."""
    db.append(user)
    logging.debug("%s", user)
    return {"id": user.id}


@router.get("/", tags=["Users"], status_code=202)
async def get_users():
    """Get users."""
    logging.debug("%s", db)
    return db


@router.delete("/{user_id}", tags=["Users"], status_code=200)
async def delete_user(user_id: UUID):
    """Delete User."""
    for user in db:
        if user.id == user_id:
            db.remove(user)
        logging.debug("%s", user)
        return user
    raise HTTPException(
        status_code=404, detail=f"Delete user failed, id {user_id} not found."
    )


@router.put("/{user_id}", tags=["Users"], status_code=202)
async def update_user(user_update: UpdateUser, user_id: UUID):
    """Update User."""
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
        logging.debug("%s", user)
        return user.id
    raise HTTPException(
        status_code=404, detail=f"Could not find user with id: {user_id}"
    )
