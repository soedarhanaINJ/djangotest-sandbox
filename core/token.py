from datetime import datetime, timedelta, timezone

from django.conf import settings
from jwt import DecodeError, ExpiredSignatureError, PyJWT


def create_token(data: dict, expiry: timedelta) -> str:
    created = datetime.now(timezone.utc)
    expired = created + expiry
    payload = {
        "iat": int(created.timestamp()),
        "exp": int(expired.timestamp()),
    }
    payload.update(data)

    instance = PyJWT()
    encoded = instance.encode(payload, settings.SECRET_KEY)
    return encoded


def decode_token(token: str) -> dict:
    instance = PyJWT()
    try:
        decoded = instance.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
    except DecodeError as e:
        print(e)
        raise ValueError("Token tidak valid")
    except ExpiredSignatureError:
        raise ValueError("Token sudah kedaluwarsa")
    except Exception as e:
        raise ValueError(str(e))

    return decoded
