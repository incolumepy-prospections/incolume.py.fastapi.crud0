import json
import re
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, Json, validator

from config import settings
from incolume.py.fastapi.crud0.controllers.utils import Role


class AccessToken(BaseModel):
    access_token: str
    expiration: str
    type: str


class ItemBase(BaseModel):
    title: str
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: list[datetime] | None = None
    description: str | None = None


class ItemCreate(ItemBase):
    class Config:
        orm_mode = True


class Item(ItemBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    email: EmailStr | None = None
    full_name: str | None = Field(
        min_length=3,
        max_length=255,
        # regex=r'^[A-ZÃÉÇÍÁ]{3,}((\s[A-Z]{2})?'
        #       r'\s[A-ZÃÉÇÍÁ]{3,}(\s[EVDI]+)?){1,}$'
    )
    roles: Role = Field(default=Role.USER)
    is_active: bool = Field(default=True)

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str = Field(min_length=8)
    
    @validator("username")
    def check_username(cls, value):
        if not re.match(settings.REGEX_USERNAME, value):
            raise ValueError("Invalide format for username")
        return value

    @validator("password")
    def check_password(cls, value):
        if not re.match(settings.REGEX_PASSWORD, value):
            raise ValueError("Invalide format for password")
        return value


class UserCreate(UserLogin):
    pass


class UserIn(UserLogin):
    pass

class UserOut(UserBase):
    is_active: bool = Field(default=True)


class UserInDB(UserBase):
    pw_hash: str = Field(alias="password")

    @validator("pw_hash")
    def gen_pw_hash(cls, value):
        return value

    class Config:
        allow_population_by_field_name = True


class UserUpdate(UserBase):
    username: Optional[str] = ""
    email: Optional[EmailStr] = ""
    roles: Optional[Role] = Field(default=Role.USER)
    is_active: Optional[bool] = Field(default=True)
