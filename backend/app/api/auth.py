# backend/app/api/auth.py — регистрация и вход
# Назначение: простая авторизация БЕЗ JWT

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.core.passwords import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterIn, LoginIn

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterIn,
    db: AsyncSession = Depends(get_async_session),
):
    """Регистрация пользователя."""

    exists = await db.execute(
        select(User).where(User.email == data.email)
    )
    if exists.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Пользователь уже существует",
        )

    user = User(
        name=data.name,
        phone=data.phone,
        email=data.email,
        password_hash=hash_password(data.password),
        card_number=f"CARD-{data.phone[-6:]}",  # (я добавил)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "user_id": user.id,  # (я добавил)
    }


@router.post("/login")
async def login(
    data: LoginIn,
    db: AsyncSession = Depends(get_async_session),
):
    """Вход пользователя."""

    res = await db.execute(
        select(User).where(User.email == data.email)
    )
    user = res.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    return {
        "user_id": user.id,  # (я добавил)
    }


@router.get("/me")
async def auth_me(
    x_user_id: int = Header(
        ...,
        alias="X-User-Id",
        convert_underscores=False,  # (я добавил)
    ),
    db: AsyncSession = Depends(get_async_session),
):
    """Текущий пользователь (роль)."""

    user = await db.get(User, x_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return {
        "id": user.id,
        "is_admin": user.is_admin,
    }
