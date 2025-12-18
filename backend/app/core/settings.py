# backend/app/core/settings.py — настройки приложения

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки backend-приложения."""

    APP_NAME: str = "FOMINYH_WEBSITE"
    DEBUG: bool = True

    # PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fominyh_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # Security
    SECRET_KEY: str = "change_me"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# ❗ ОБЯЗАТЕЛЬНО: экземпляр настроек
settings = Settings()  # (я добавил)
