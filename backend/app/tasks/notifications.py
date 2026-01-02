# backend/app/tasks/notifications.py — задачи уведомлений
# Назначение: Celery-задачи уведомлений (заглушки)

from time import sleep
from datetime import datetime, timedelta
import asyncio

from celery import shared_task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import get_engine
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
    """

    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    async def _check():
        engine = get_engine()

        async_session = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with async_session() as session:
            result = await session.execute(
                select(Booking).where(
                    Booking.start_time >= now,
                    Booking.start_time <= tomorrow,
                )
            )
            bookings = result.scalars().all()

            for booking in bookings:
                # TODO: отправка email / telegram
                print(f"[CELERY][BEAT] Upcoming booking: {booking.id}")

    asyncio.run(_check())
