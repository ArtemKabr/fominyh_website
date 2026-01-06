# backend/app/api/auth.py — регистрация и логин
# Назначение: регистрация пользователей, логин пользователей и администраторов

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.passwords import hash_password, verify_password
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import RegisterIn, LoginIn, AdminLoginIn, TokenOut
from app.services.auth import authenticate_admin  # (я добавил)
from app.core.security import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterIn,
    db: AsyncSession = Depends(get_async_session),
) -> TokenOut:
    """Регистрация пользователя."""  # (я добавил)

    res = await db.execute(select(User).where(User.email == payload.email))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user = User(
        name=payload.name,        # (я добавил)
        phone=payload.phone,      # (я добавил)
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_admin=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=user.id)
    return TokenOut(access_token=token, token_type="bearer")


@router.post("/login", response_model=TokenOut)
async def login(
    payload: LoginIn,
    db: AsyncSession = Depends(get_async_session),
) -> TokenOut:
    """Логин пользователя по email."""  # (я добавил)

    res = await db.execute(
        select(User).where(User.email == payload.email)  # (я добавил)
    )
    user = res.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
        )

    token = create_access_token(subject=user.id)
    return TokenOut(access_token=token, token_type="bearer")


@router.post("/admin/login", response_model=TokenOut)  # (я добавил)
async def admin_login(
    payload: AdminLoginIn,
    db: AsyncSession = Depends(get_async_session),
) -> TokenOut:
    """Логин администратора."""  # (я добавил)

    admin = await authenticate_admin(
        db,
        email=payload.email,
        password=payload.password,
    )

    token = create_access_token(subject=admin.id)
    return TokenOut(access_token=token, token_type="bearer")


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    """Текущий пользователь по JWT."""  # (я добавил)
    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "is_admin": user.is_admin,
    }
