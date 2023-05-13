"""Module auth."""

import logging
import inspect
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import NamedTemporaryFile

import pyotp
import qrcode
from fastapi import Depends, Response, status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import settings
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0.models import UserModel
from incolume.py.fastapi.crud0.schemas import AccessToken, UserLogin, oauth2

crypt_context = CryptContext(schemes=["sha256_crypt"])


def obter_usuario_logado(
    token: str = Depends(oauth2), session: Session = Depends(get_db_session())
):
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
    db: Session = Depends(get_db_session), token=Depends(oauth2)
):
    """Token verifier."""
    Auth(db).is_valid_token(access_token=token)


class Auth:
    """Class Auth."""

    def __init__(self, db_session: Session) -> None:
        """Class init."""
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
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
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
        """Verify is valid token."""
        logging.debug(f"{access_token}")
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
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        raise NotImplementedError(f'Ops: {inspect.stack()[0][3]} not yet.')

    @staticmethod
    def generate_token(user, seconds=30, minutes=0, hours=0, days=0, weeks=0):
        """Generate JWT token."""
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
    """Class Auth OTP."""

    def __init__(self, db_session: Session) -> None:
        """Class init."""
        self.db_session = db_session
        self.totp = pyotp.TOTP(settings.otp_key)
        self.otp_title = settings.otp_title

    def login(self, user_in: UserLogin):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
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
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        return self.totp.now()

    def _is_valid_otp(self, pw_otp):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        return self.totp.verify(pw_otp)

    def _generate_uri(self, user: UserLogin, title: str = ""):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        return self.totp.provisioning_uri(
            name=user.email, issuer_name=title or settings.otp_title
        )

    def get_qr_otp_file(self, user: UserModel):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        qr = qrcode.make(self._generate_uri(user))
        fout = Path(NamedTemporaryFile(prefix="qr_", suffix=".png").name)
        qr.save(fout.as_posix())
