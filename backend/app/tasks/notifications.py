# backend/app/tasks/notifications.py — celery-задачи уведомлений
# Назначение: уведомления пользователям и админу (Telegram / email)

import asyncio
from datetime import datetime, timedelta

from sqlalchemy import select  # (я добавил)

from app.core.celery_app import celery_app
from app.core.database import get_async_session
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.models.service import Service
from app.core.settings import settings
from app.services.telegram import send_telegram_message

# -------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -------------------------------------------------


async def _get_booking_context(booking_id: int):
    """Загрузить связанные данные для уведомлений."""  # (я добавил)
    async for session in get_async_session():
        booking = await session.get(Booking, booking_id)
        if not booking:
            return None

        user = await session.get(User, booking.user_id)
        service = await session.get(Service, booking.service_id)

        return booking, user, service


async def _send_telegram(chat_id: int, text: str) -> None:
    """Отправка сообщения в Telegram."""
    await send_telegram_message(chat_id, text)  # (я добавил)


async def _send_email(email: str, subject: str, body: str) -> None:
    """Отправка email (заглушка)."""  # (я добавил)
    print(f"[email] to={email}: {subject}")


# -------------------------------------------------
# УВЕДОМЛЕНИЯ О СОЗДАНИИ ЗАПИСИ
# -------------------------------------------------


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def send_booking_created(self, booking_id: int) -> None:
    """Уведомление о создании записи."""  # (я добавил)

    async def _run():
        ctx = await _get_booking_context(booking_id)
        if not ctx:
            return

        booking, user, service = ctx

        text = (
            f"📌 Новая запись\n"
            f"Услуга: {service.name}\n"
            f"Дата: {booking.start_time:%d.%m.%Y %H:%M}\n"  # (я добавил)
            f"Телефон: {user.phone}"
        )

        if settings.admin_telegram_chat_id:
            await _send_telegram(settings.admin_telegram_chat_id, text)

        if user.telegram_chat_id:
            await _send_telegram(user.telegram_chat_id, "✅ Вы успешно записались")

        await _send_email(
            user.email,
            "Запись подтверждена",
            f"Вы записаны на {service.name} {booking.start_time:%d.%m.%Y %H:%M}",  # (я добавил)
        )

    asyncio.run(_run())


# -------------------------------------------------
# УВЕДОМЛЕНИЕ ОБ ОТМЕНЕ
# -------------------------------------------------


@celery_app.task(bind=True)
def send_booking_canceled(self, booking_id: int) -> None:
    """Уведомление об отмене записи."""  # (я добавил)

    async def _run():
        ctx = await _get_booking_context(booking_id)
        if not ctx:
            return

        booking, user, service = ctx

        text = (
            f"❌ Запись отменена\n"
            f"Услуга: {service.name}\n"
            f"Дата: {booking.start_time:%d.%m.%Y %H:%M}"  # (я добавил)
        )

        if user.telegram_chat_id:
            await _send_telegram(user.telegram_chat_id, text)

        if user.email:
            await _send_email(user.email, "Запись отменена", text)

    asyncio.run(_run())


# -------------------------------------------------
# НАПОМИНАНИЯ
# -------------------------------------------------


@celery_app.task(bind=True)
def send_booking_reminder(self, booking_id: int, hours: int) -> None:
    """Напоминание о записи за N часов."""  # (я добавил)

    async def _run():
        ctx = await _get_booking_context(booking_id)
        if not ctx:
            return

        booking, user, service = ctx

        if booking.status != BookingStatus.ACTIVE.value:
            return

        text = (
            f"⏰ Напоминание\n"
            f"Через {hours} ч. у вас запись:\n"
            f"{service.name}\n"
            f"{booking.start_time:%d.%m.%Y %H:%M}"  # (я добавил)
        )

        if user.telegram_chat_id:
            await _send_telegram(user.telegram_chat_id, text)

    asyncio.run(_run())


# -------------------------------------------------
# ПРОВЕРКА БЛИЖАЙШИХ ЗАПИСЕЙ (beat)
# -------------------------------------------------


@celery_app.task(name="app.tasks.notifications.check_upcoming_bookings")
def check_upcoming_bookings() -> None:
    """Поиск записей для напоминаний."""  # (я добавил)

    async def _run():
        now = datetime.now()
        notify_at = now + timedelta(minutes=5)

        async for session in get_async_session():
            result = await session.execute(
                select(Booking).where(
                    Booking.status == BookingStatus.ACTIVE.value,
                    Booking.start_time >= now,  # (я добавил)
                    Booking.start_time <= notify_at,  # (я добавил)
                )
            )

            for booking in result.scalars().all():
                send_booking_reminder.delay(booking.id, hours=2)

    asyncio.run(_run())
