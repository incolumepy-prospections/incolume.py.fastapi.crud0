"""Module schemas."""
import json
import re
import uuid
from datetime import datetime
from inspect import stack
from typing import Any, Optional

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field, Json, validator

from config import settings
from incolume.py.fastapi.crud0.controllers.utils import Role

oauth2: Any = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AccessToken(BaseModel):
    """schema for access token."""

    access_token: str
    expiration: str
    type: str


class ItemBase(BaseModel):
    """schema for item base."""

    title: str
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: list[datetime] | None = None
    description: str | None = None


class ItemCreate(ItemBase):
    """schema for item creation."""

    class Config:
        """Configuration for Superclass."""

        orm_mode = True


class Item(ItemBase):
    """schema for item."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    owner_id: int

    class Config:
        """Configuration for Superclass."""

        orm_mode = True


class UserBase(BaseModel):
    """schema for user base."""

    username: str = Field(min_length=3, max_length=255)
    email: EmailStr | None = None
    full_name: str | None = Field(
        min_length=3,
        max_length=255,
        # regex=settings.regex_fullname
    )
    is_active: bool = Field(default=True)

    class Config:
        """Configuration for Superclass."""

        orm_mode = True


class UserLogin(UserBase):
    """schema for user login."""

    password: str = Field(min_length=8)

    @validator("username")
    def check_username(cls, value):
        """Validate {}.""".format(stack()[0][3])
        if not re.match(settings.REGEX_USERNAME, value):
            raise ValueError("Invalide format for username")
        return value

    @validator("password")
    def check_password(cls, value):
        """Validate {}.""".format(stack()[0][3])
        if not re.match(settings.REGEX_PASSWORD, value):
            raise ValueError("Invalide format for password")
        return value


class UserCreate(UserLogin):
    """schema for user creation."""

    class Config:
        """Config for UserCreate."""

        schema_extra = {
            "example": {
                "username": "user",
                "email": "user@example.com",
                "full_name": "Full Name for User of System",
                "is_active": True,
                "password": "aaQQ!!11",
            }
        }


class UserIn(UserLogin):
    """schema for user in."""


class UserOut(UserBase):
    """schema for user out."""

    roles: Role = Field(default=Role.USER)
    is_active: bool = Field(default=True)


class UserInDB(UserBase):
    """schema for user in DB."""

    pw_hash: str = Field(alias="password")

    @validator("pw_hash")
    def gen_pw_hash(cls, value):
        """Validate {}.""".format(stack()[0][3])
        return value

    class Config:
        """Configuration for Superclass."""

        allow_population_by_field_name = True


class UserUpdate(UserBase):
    """schema for user updating."""

    full_name: Optional[str] = ""
    username: Optional[str] = ""
    email: Optional[EmailStr] = ""

    class Config:
        """configuration for superclass."""

        schema_extra = {
            "example": {
                "username": "user",
                "email": "user@example.com",
                "full_name": "Full Name for User of System",
            }
        }
