# backend/app/services/auth.py — сервис авторизации
# отвечает только за бизнес-логику проверки пользователя / администратора

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.passwords import verify_password
from app.core.errors import AUTH_INVALID_CREDENTIALS, AUTH_FORBIDDEN  # (я добавил)
from app.models.user import User


async def authenticate_admin(
    db: AsyncSession,
    *,
    email: str,
    password: str,
) -> User:
    """
    Проверить email + password и is_admin.
    JWT здесь НЕ создаётся — только бизнес-проверка.
    """  # (я добавил)

    result = await db.execute(
        select(User).where(User.email == email)
    )  # (я добавил)
    user = result.scalar_one_or_none()  # (я добавил)

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail=AUTH_INVALID_CREDENTIALS,  # (я добавил)
        )  # (я добавил)

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail=AUTH_FORBIDDEN,  # (я добавил)
        )  # (я добавил)

    return user  # (я добавил)
