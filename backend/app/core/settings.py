# backend/app/core/settings.py — настройки приложения

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # App
    app_name: str = "FOMINYH WEBSITE"
    debug: bool = False

    # Admin
    admin_token: str  # (я добавил)

    # Database
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # Celery / Redis
    celery_broker_url: str | None = None  # (я добавил)
    celery_result_backend: str | None = None  # (я добавил)

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


settings = Settings()
