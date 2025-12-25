# backend/app/core/celery_app.py — конфигурация Celery

from celery import Celery
from app.core.settings import settings

celery_app = Celery(
    "fominyh_backend",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# ЯВНЫЙ импорт задач (важно)
import app.tasks  # (я добавил)
