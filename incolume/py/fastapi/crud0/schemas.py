import re
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from config import settings


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
    username: str
    email: EmailStr | None = None
    full_name: str | None = None

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str


class UserIn(UserLogin):
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


class UserOut(UserBase):
    is_active: bool = Field(default=True)
    pass


class UserInDB(UserBase):
    pw_hash: str = Field(alias="password")

    @validator("pw_hash")
    def gen_pw_hash(cls, value):
        return value

    class Config:
        allow_population_by_field_name = True
