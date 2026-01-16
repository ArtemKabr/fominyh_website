# backend/app/bot/states/booking.py — FSM записи
# Назначение: состояния бронирования через Telegram

from aiogram.fsm.state import State, StatesGroup


class BookingFlow(StatesGroup):
    choose_service = State()
    choose_date = State()
    choose_slot = State()
