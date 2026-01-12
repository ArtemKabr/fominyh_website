# backend/app/bot/dispatcher.py — инициализация bot и dispatcher

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.core.settings import settings
from app.bot.handlers.admin_confirm import router as admin_router
from app.bot.handlers.user_start import router as user_router

bot = Bot(
    token=settings.telegram_api_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)

dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(admin_router)
