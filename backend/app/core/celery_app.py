# backend/app/core/celery_app.py — конфигурация Celery
# Назначение: инициализация Celery (broker/backend), регистрация задач, beat

from celery import Celery
from celery.schedules import crontab

from app.core.settings import settings


BROKER_URL = settings.celery_broker_url or "redis://redis:6379/0"  #
RESULT_BACKEND = settings.celery_result_backend or "redis://redis:6379/1"  #


celery_app = Celery(
    "fominyh_backend",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

celery_app.conf.update(
    timezone="Europe/Moscow",
    enable_utc=False,
)

celery_app.conf.beat_schedule = {
    "check-upcoming-bookings": {
        "task": "app.tasks.notifications.check_upcoming_bookings",
        "schedule": crontab(minute="*/5"),
    },
}

# гарантируем регистрацию задач
import app.tasks.notifications  # noqa: E402,F401

__all__ = ["celery_app"]
