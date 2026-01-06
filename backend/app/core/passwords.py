# backend/app/core/passwords.py — хеширование паролей

from passlib.context import CryptContext

_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Создать bcrypt-хеш пароля (ограничение 72 байта)."""
    password = password.encode("utf-8")[:72].decode("utf-8")  # я добавил
    return _pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Проверить пароль."""
    password = password.encode("utf-8")[:72].decode("utf-8")  # я добавил
    return _pwd_context.verify(password, password_hash)
