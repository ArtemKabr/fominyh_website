# backend/app/core/security.py — JWT и безопасность
# Назначение: создание и проверка access-токенов, права доступа

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.database import get_async_session
from app.models.user import User
from app.core.errors import AUTH_FORBIDDEN

bearer_scheme = HTTPBearer(auto_error=False)  # (я добавил)


def create_access_token(
    subject: int,
    expires_delta: timedelta | None = None,
) -> str:
    """Создать JWT access token."""  # (я добавил)

    now = datetime.now(timezone.utc)

    expire = (
        now + expires_delta
        if expires_delta
        else now + timedelta(minutes=settings.access_token_exp_minutes)
    )

    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    """Получить пользователя из JWT."""  # (я добавил)

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id_raw = payload.get("sub")
        if not user_id_raw:
            raise ValueError
        user_id = int(user_id_raw)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )

    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )

    return user


async def admin_required(
    user: User = Depends(get_current_user),
) -> User:
    """Проверка прав администратора."""  # (я добавил)

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=AUTH_FORBIDDEN,
        )

    return user
