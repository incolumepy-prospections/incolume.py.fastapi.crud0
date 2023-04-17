from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError

from incolume.py.fastapi.crud0.schemas import UserIn
from incolume.py.fastapi.crud0.models import UserModel
from config import settings


crypt_context = CryptContext(schemes=['sha256_crypt'])


class Auth:
    def login(self, user:UserIn, seconds: int = 30, minutes: int = 0, hours: int = 0, days: int = 0, weeks: int = 0):
        user_login = self.db_session.query(UserModel).filter_by(username=user.username)

        if not user_login or not crypt_context.verify(secret=user.password, hash=user_login.pw_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTORIZED, detail='Invalid username or password')
        
        exp = datetime.utcnow() + timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)
        payload = {
            'sub': user.username,
            'exp': exp,
        }

        access_token = jwt.encode(payload, settings.secret_key, algorithm=settings.ALGORITHM)

        return {
            'access_token': access_token,
            'expiration': exp
        }

    def logout(self):
        pass

    def verify_token(self):
        pass

    def generate_token(self):
        pass
