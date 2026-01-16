# backend/app/bot/utils/notify_admin.py
# Назначение: уведомление админа о новой записи

from app.bot.bot import bot
from app.bot.keyboards.admin import admin_confirm_booking_kb
from app.core.settings import settings
from app.models.booking import Booking


async def notify_admin_new_booking(booking: Booking) -> None:
    """Отправить админу новую запись."""  # (я добавил)

    text = (
        "📅 Новая запись с сайта\n\n"
        f"ID: #{booking.id}\n"
        f"Услуга: {booking.service_id}\n"
        f"Время: {booking.start_time.strftime('%d.%m.%Y %H:%M')}\n"
        f"Статус: {booking.status}"
    )

    await bot.send_message(
        chat_id=settings.ADMIN_TELEGRAM_CHAT_ID,
        text=text,
        reply_markup=admin_confirm_booking_kb(booking.id),
    )
