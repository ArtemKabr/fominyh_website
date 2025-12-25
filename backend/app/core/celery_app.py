# backend/app/core/celery_app.py — конфигурация Celery и Beat

from celery import Celery
from celery.schedules import crontab

from app.core.settings import settings

celery_app = Celery(
    "fominyh_backend",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Базовая конфигурация Celery  # (я добавил)
celery_app.conf.update(
    timezone="Europe/Moscow",  # (я добавил)
    enable_utc=False,          # (я добавил)
)

# Celery Beat — периодические задачи  # (я добавил)
celery_app.conf.beat_schedule = {
    "check-bookings-reminders-every-5-minutes": {
        "task": "app.tasks.notifications.check_upcoming_bookings",
        "schedule": crontab(minute="*/5"),
    },
}

# ЯВНЫЙ импорт задач (обязательно)
import app.tasks.notifications  # noqa: F401,E402  # (я добавил)
