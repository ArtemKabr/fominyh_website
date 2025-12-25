# backend/app/tasks/notifications.py — задачи уведомлений

from time import sleep
from celery import shared_task


@shared_task(
    name="app.tasks.notifications.send_booking_created",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def send_booking_created(booking_id: int):
    """
    Уведомление о создании записи.
    Пока заглушка.
    """
    sleep(1)
    print(f"[CELERY] Booking created: {booking_id}")
