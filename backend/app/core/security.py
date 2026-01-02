# backend/app/core/security.py — JWT и безопасность
# отвечает за создание и проверку access-токенов

from datetime import datetime, timedelta
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

# JWT настройки
SECRET_KEY = "CHANGE_ME_SECRET_KEY"  # (я добавил)
ALGORITHM = "HS256"  # (я добавил)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # (я добавил)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")  # (я добавил)


def create_access_token(
    subject: int,
    expires_delta: timedelta | None = None,
) -> str:
    """Создать JWT access token."""  # (я добавил)

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode: dict[str, Any] = {
        "exp": expire,
        "sub": subject,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt
