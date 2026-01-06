# backend/app/schemas/auth.py — схемы авторизации

from pydantic import BaseModel, EmailStr


class RegisterIn(BaseModel):
    """Входные данные регистрации пользователя."""  # (я изменил)
    name: str  # (я добавил)
    phone: str  # (я добавил)
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    """Входные данные логина пользователя."""
    email: EmailStr
    password: str


class AdminLoginIn(BaseModel):
    """Входные данные логина администратора."""  # (я добавил)
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    """Ответ с JWT токеном."""
    access_token: str
    token_type: str = "bearer"
