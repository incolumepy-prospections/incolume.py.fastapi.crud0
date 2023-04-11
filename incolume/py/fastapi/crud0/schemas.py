import re
from pydantic import BaseModel, EmailStr, validator
from config import settings


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

    @validator('username')
    def check_username(cls, value):
        if not re.match(settings.REGEX_USERNAME, value):
            raise ValueError('Invalide format for username')
        return value
    
    class Config:
        orm_mode = True


class UserIn(UserBase):
    password: str

    @validator('password')
    def check_password(cls, value):
        if not re.match(settings.REGEX_PASSWORD, value):
            raise ValueError('Invalide format for password')
        return value

class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    pw_hash: str
