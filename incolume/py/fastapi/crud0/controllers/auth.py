import logging
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import NamedTemporaryFile

import pyotp
import qrcode
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import settings
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0.models import UserModel
from incolume.py.fastapi.crud0.schemas import AccessToken, UserLogin

crypt_context = CryptContext(schemes=["sha256_crypt"])
oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obter_usuario_logado(token: str = Depends(oauth),
                         session: Session = Depends(get_db_session())):
    """Get user logged."""
    # exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    #
    # try:
    #     telefone = token_provider.verificar_access_token(token)
    # except JWTError:
    #     raise exception
    #
    # if not telefone:
    #     raise exception
    #
    # usuario = RepositorioUsuario(session).obter_por_telefone(telefone)
    #
    # if not usuario:
    #     raise exception
    #
    # return usuario

    pass


def token_verifier(
    db: Session = Depends(get_db_session), token=Depends(oauth)
):
    Auth(db).is_valid_token(access_token=token)


class Auth:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def login(
        self,
        user: UserLogin,
        seconds: int = 30,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
    ):
        logging.debug(
            f"{user=}, {seconds=}, {minutes=}, {hours=}, {days=}, {weeks=}"
        )

        user_login = (
            self.db_session.query(UserModel)
            .filter_by(username=user.username)
            .first()
        )
        if not user_login or not crypt_context.verify(
            secret=user.password, hash=user_login.pw_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        logging.debug(f"{user_login.__dict__=}")

        access_token = self.generate_token(
            user, seconds, minutes, hours, days, weeks
        )

        logging.debug(f"{access_token=}")
        return access_token

    def is_valid_token(self, access_token: str):
        try:
            data = jwt.decode(
                access_token,
                settings.secret_key,
                algorithms=[settings.algorithm],
            )
        except JWTError as e:
            logging.error(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        user_logged = (
            self.db_session.query(UserModel)
            .filter_by(username=data["sub"])
            .first()
        )
        if not user_logged:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        return True

    def logout(self):
        pass

    def generate_token(
        self, user, seconds=30, minutes=0, hours=0, days=0, weeks=0
    ):
        exp = datetime.utcnow() + timedelta(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks,
        )
        payload = {
            "sub": user.username,
            "exp": exp,
        }
        logging.debug(f"{payload=}")

        access_token = jwt.encode(
            payload, settings.secret_key, algorithm=settings.ALGORITHM
        )

        return AccessToken(
            access_token=access_token,
            expiration=exp.isoformat(),
            type="bearer",
        )


class AuthOTP:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.totp = pyotp.TOTP(settings.otp_key)
        self.otp_title = settings.otp_title

    def login(self, user_in: UserLogin):
        user_login = (
            self.db_session.query(UserModel)
            .filter_by(username=user_in.username)
            .first()
        )
        if not user_login or not self._is_valid_otp(user_in.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )
        return user_login

    def get_pw_otp(self):
        return self.totp.now()

    def _is_valid_otp(self, pw_otp):
        return self.totp.verify(pw_otp)

    def _generate_uri(self, user: UserLogin, title: str = ""):
        return self.totp.provisioning_uri(
            name=user.email, issuer_name=title or settings.otp_title
        )

    def get_qr_otp_file(self, user: UserModel):
        qr = qrcode.make(self._generate_uri(user))
        fout = Path(NamedTemporaryFile(prefix="qr_", suffix=".png").name)
        qr.save(fout.as_posix())
