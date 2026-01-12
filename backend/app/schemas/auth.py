# backend/app/schemas/auth.py — схемы авторизации
# Назначение: регистрация, логин, восстановление пароля

from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    """Регистрация пользователя."""

    name: str = Field(..., min_length=1)
    phone: str
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginIn(BaseModel):
    """Логин пользователя."""

    email: EmailStr
    password: str


class AdminLoginIn(BaseModel):
    """Логин администратора."""

    email: EmailStr
    password: str


class TokenOut(BaseModel):
    """JWT токен."""

    access_token: str
    token_type: str


# ===== ВОССТАНОВЛЕНИЕ ПАРОЛЯ =====


class ForgotPasswordIn(BaseModel):
    """Запрос сброса пароля."""

    email: EmailStr


class ResetPasswordIn(BaseModel):
    """Сброс пароля по токену."""

    token: str
    new_password: str = Field(..., min_length=8)
