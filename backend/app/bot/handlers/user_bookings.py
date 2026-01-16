# backend/app/bot/handlers/user_booking.py — бронирование
# Назначение: запись пользователя через Telegram

from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.service import Service
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.bot.states.booking import BookingFlow
from app.bot.keyboards.booking import services_kb, dates_kb, slots_kb
from app.bot.keyboards.user import user_main_menu_kb
from app.services.booking import get_free_slots

router = Router()


@router.callback_query(F.data == "user:book")
async def start_booking(cb: CallbackQuery, state: FSMContext) -> None:
    async with async_session_maker() as session:
        rows = (await session.execute(
            select(Service.id, Service.name)
        )).all()

    if not rows:
        await cb.message.edit_text(
            "Услуг пока нет.",
            reply_markup=user_main_menu_kb(),
        )
        await cb.answer()
        return

    await state.set_state(BookingFlow.choose_service)
    await cb.message.edit_text(
        "Выберите услугу:",
        reply_markup=services_kb(rows),
    )
    await cb.answer()


@router.callback_query(
    BookingFlow.choose_service,
    F.data.startswith("book:svc:"),
)
async def choose_service(cb: CallbackQuery, state: FSMContext) -> None:
    service_id = int(cb.data.split(":")[-1])
    await state.update_data(service_id=service_id)

    await state.set_state(BookingFlow.choose_date)
    await cb.message.edit_text(
        "Выберите дату:",
        reply_markup=dates_kb(),
    )
    await cb.answer()


@router.callback_query(
    BookingFlow.choose_date,
    F.data.startswith("book:date:"),
)
async def choose_date(cb: CallbackQuery, state: FSMContext) -> None:
    date_iso = cb.data.split(":")[-1]
    await state.update_data(date=date_iso)

    day = datetime.fromisoformat(date_iso).date()
    data = await state.get_data()
    service_id = data["service_id"]

    async with async_session_maker() as session:
        free_slots_dt = await get_free_slots(
            session,
            day=day,
            service_id=service_id,
        )

    if not free_slots_dt:
        await cb.message.edit_text(
            "❌ На выбранную дату нет свободных слотов.",
            reply_markup=user_main_menu_kb(),
        )
        await state.clear()
        await cb.answer()
        return

    slots = [
        (dt.strftime("%H:%M"), i + 1)
        for i, dt in enumerate(free_slots_dt)
    ]

    await state.update_data(slots=[dt.isoformat() for dt in free_slots_dt])
    await state.set_state(BookingFlow.choose_slot)

    await cb.message.edit_text(
        "Выберите время:",
        reply_markup=slots_kb(slots),
    )
    await cb.answer()


@router.callback_query(
    BookingFlow.choose_slot,
    F.data.startswith("book:slot:"),
)
async def choose_slot(cb: CallbackQuery, state: FSMContext) -> None:
    slot_index = int(cb.data.split(":")[-1]) - 1
    data = await state.get_data()

    slots = data["slots"]
    start_time = datetime.fromisoformat(slots[slot_index])
    service_id = data["service_id"]

    async with async_session_maker() as session:
        user = await session.scalar(
            select(User).where(
                User.telegram_chat_id == cb.from_user.id
            )
        )

        if not user:
            await cb.message.edit_text("Пользователь не найден. /start")
            await cb.answer()
            return

        booking = Booking(
            user_id=user.id,
            service_id=service_id,
            start_time=start_time,
            status=BookingStatus.PENDING.value,
        )

        session.add(booking)
        await session.commit()

    await state.clear()
    await cb.message.edit_text(
        "✅ Запись создана и ожидает подтверждения.",
        reply_markup=user_main_menu_kb(),
    )
    await cb.answer()
