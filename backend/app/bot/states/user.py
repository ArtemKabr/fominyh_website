# backend/app/bot/states/user.py
# Назначение: состояния пользователя Telegram

from aiogram.fsm.state import State, StatesGroup


class UserRegister(StatesGroup):
    waiting_for_phone = State()
