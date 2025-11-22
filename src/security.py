"""Funções de utilidade para segurança, como hashing de senhas e JWT."""

from datetime import UTC, datetime, timedelta
from typing import Any

from argon2 import PasswordHasher
from jose import jwt

from config import settings

ph = PasswordHasher()


def get_password_hash(plain_password: str) -> str:
    """Gera o hash de uma senha em texto plano.

    Args:
        plain_password: A senha em texto plano a ser hasheada.

    Returns:
        O hash da senha.

    """
    return ph.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash.

    Args:
        plain_password: A senha em texto plano.
        password_hash: O hash da senha a ser verificado.

    Returns:
        True se a senha corresponder ao hash, False caso contrário.

    """
    try:
        return ph.verify(password_hash, plain_password)
    except Exception:  # noqa: BLE001
        return False


def create_access_token(
    subject: str | int, expires_minutes: int | None = None
) -> str:
    """Cria um token de acesso JWT.

    Args:
        subject: O assunto do token (geralmente o ID do usuário).
        expires_minutes: Tempo de expiração em minutos. Se não for
            fornecido, usa o padrão das configurações.

    Returns:
        O token de acesso JWT como uma string.

    """
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes or settings.jwt_expire_minutes
    )
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}

    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
