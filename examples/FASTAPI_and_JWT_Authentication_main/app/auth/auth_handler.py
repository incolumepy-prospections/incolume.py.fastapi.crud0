# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

from jose import JWTError, jwt

from config import settings

JWT_SECRET = settings.secret_key
JWT_ALGORITHM = settings["algorithm"]


def token_response(token: str):
    return {"access_token": token}


# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        return (
            decoded_token if decoded_token["expires"] >= time.time() else None
        )
    except:
        return {}
