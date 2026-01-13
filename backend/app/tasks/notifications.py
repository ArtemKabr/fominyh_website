# backend/app/tasks/notifications.py — celery-задачи уведомлений
# Назначение: уведомления пользователям и админу (Telegram / email)

import asyncio

from celery import shared_task

from app.core.database import async_session_maker
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.models.service import Service
from app.core.settings import settings


# -------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -------------------------------------------------


async def _get_booking_context(booking_id: int):
    """Загрузить связанные данные для уведомлений."""  # 

    async with async_session_maker() as session:
        booking = await session.get(Booking, booking_id)
        if not booking:
            return None

        user = await session.get(User, booking.user_id)
        service = await session.get(Service, booking.service_id)

        return booking, user, service


async def _send_telegram(chat_id: int, text: str) -> None:
    """Отправка сообщения в Telegram (заглушка)."""  # 
    # TODO: подключить aiogram / requests
    print(f"[telegram] chat_id={chat_id}: {text}")


async def _send_email(email: str, subject: str, body: str) -> None:
    """Отправка email (заглушка)."""  # 
    # TODO: SMTP / SendGrid
    print(f"[email] to={email}: {subject}")


# -------------------------------------------------
# УВЕДОМЛЕНИЯ О СОЗДАНИИ ЗАПИСИ
# -------------------------------------------------


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 10})
def send_booking_created(self, booking_id: int) -> None:
    """Уведомление о создании записи."""  # 

    async def _run():
        ctx = await _get_booking_context(booking_id)
        if not ctx:
            return

        booking, user, service = ctx

        text = (
            f"📌 Новая запись\n"
            f"Услуга: {service.name}\n"
            f"Дата: {booking.start_time:%d.%m.%Y %H:%M}\n"
            f"Телефон: {user.phone}"
        )

        # админу
        if settings.admin_telegram_chat_id:
            await _send_telegram(settings.admin_telegram_chat_id, text)

        # пользователю
        if user.telegram_chat_id:
            await _send_telegram(user.telegram_chat_id, "✅ Вы успешно записались")

        if user.email:
            await _send_email(
                user.email,
                "Запись подтверждена",
                f"Вы записаны на {service.name} {booking.start_time:%d.%m.%Y %H:%M}",
            )

    asyncio.run(_run())


# -------------------------------------------------
# УВЕДОМЛЕНИЕ ОБ ОТМЕНЕ
# -------------------------------------------------


@shared_task(bind=True)
def send_booking_canceled(self, booking_id: int) -> None:
    """Уведомление об отмене записи."""  # 

    async def _run():
        ctx = await _get_booking_context(booking_id)
        if not ctx:
            return

        booking, user, service = ctx

        text = (
            f"❌ Запись отменена\n"
            f"Услуга: {service.name}\n"
            f"Дата: {booking.start_time:%d.%m.%Y %H:%M}"
        )

        if user.telegram_chat_id:
            await _send_telegram(user.telegram_chat_id, text)

        if user.email:
            await _send_email(user.email, "Запись отменена", text)

    asyncio.run(_run())


# -------------------------------------------------
# НАПОМИНАНИЯ
# -------------------------------------------------


@shared_task(bind=True)
def send_booking_reminder(self, booking_id: int, hours: int) -> None:
    """Напоминание о записи за N часов."""  # 

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
            f"{booking.start_time:%d.%m.%Y %H:%M}"
        )

        if user.telegram_chat_id:
            await _send_telegram(user.telegram_chat_id, text)

    asyncio.run(_run())
