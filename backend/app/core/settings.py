# backend/app/core/settings.py — настройки приложения

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # App
    app_name: str = "FOMINYH WEBSITE"
    debug: bool = False

    # Database
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # Redis / Celery
    redis_host: str
    redis_port: int
    celery_broker_url: str
    celery_result_backend: str

    @property
    def database_url(self) -> str:
        """URL подключения к PostgreSQL (async)."""
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()  # (я добавил)
