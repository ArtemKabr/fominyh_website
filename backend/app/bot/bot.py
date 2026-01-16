# backend/app/bot/bot.py — инициализация Telegram-бота
# Назначение: создание Bot и Dispatcher

from aiogram import Bot, Dispatcher
from app.core.settings import settings


bot = Bot(token=settings.telegram_api_token)  # (я добавил)
dp = Dispatcher()  # (я добавил)
