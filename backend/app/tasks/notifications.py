# backend/app/tasks/notifications.py — задачи уведомлений

from time import sleep
from datetime import datetime, timedelta
import asyncio

from celery import shared_task
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.booking import Booking


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


@shared_task(
    name="app.tasks.notifications.check_upcoming_bookings",
)
def check_upcoming_bookings():
    """
    Periodic-задача (Celery Beat).
    Проверка записей на сегодня и завтра.
    """  # (я добавил)

    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    async def _check():
        async with async_session_maker() as session:
            result = await session.execute(
                select(Booking).where(
                    Booking.start_time >= now,
                    Booking.start_time <= tomorrow,
                )
            )
            bookings = result.scalars().all()

            for booking in bookings:
                # TODO: отправка email / telegram  # (я добавил)
                print(f"[CELERY][BEAT] Upcoming booking: {booking.id}")

    asyncio.run(_check())  # (я добавил)
