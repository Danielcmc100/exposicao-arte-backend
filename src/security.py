from datetime import datetime, timedelta, timezone
from typing import Any

from argon2 import PasswordHasher
from jose import jwt

from config import settings

ph = PasswordHasher()

def get_password_hash(plain_password: str) -> str:
    return ph.hash(plain_password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return ph.verify(password_hash, plain_password)
    except Exception:
        return False

def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.jwt_expire_minutes
    )
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt
