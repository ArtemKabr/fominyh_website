# backend/app/core/passwords.py — хеширование паролей

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Создать хеш пароля."""  # (я добавил)
    return _pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Проверить пароль."""  # (я добавил)
    return _pwd_context.verify(password, password_hash)
