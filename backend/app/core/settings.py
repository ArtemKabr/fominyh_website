# backend/app/core/settings.py — настройки приложения
# Назначение: централизованные настройки backend (JWT, БД, Celery, SMTP)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # --------------------
    # App
    # --------------------
    app_name: str = "FOMINYH WEBSITE"
    debug: bool = False
    testing: bool = False  # (я добавил)

    # --------------------
    # Security / JWT
    # --------------------
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 60 * 24

    # --------------------
    # Database
    # --------------------
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # --------------------
    # Celery / Redis
    # --------------------
    celery_broker_url: str
    celery_result_backend: str

    # --------------------
    # Telegram
    # --------------------
    telegram_api_token: str | None = None
    telegram_admin_chat_id: int | None = None

    # --------------------
    # SMTP (email) — optional
    # --------------------
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None

    # --------------------
    # Helpers
    # --------------------
    @property
    def database_url(self) -> str:
        """URL подключения к PostgreSQL (async)."""
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def smtp_enabled(self) -> bool:
        """Включена ли отправка почты."""
        return all(
            [
                self.smtp_host,
                self.smtp_port,
                self.smtp_user,
                self.smtp_password,
                self.smtp_from,
            ]
        )

    class Config:
        env_file = ".env"
        env_prefix = ""
        case_sensitive = False
        extra = "ignore"


settings = Settings()
