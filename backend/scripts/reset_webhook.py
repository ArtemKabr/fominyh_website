# backend/scripts/reset_webhook.py
# Назначение: сброс webhook и зависших getUpdates у Telegram

import asyncio

from aiogram import Bot

from app.core.settings import settings


async def main() -> None:
    bot = Bot(token=settings.telegram_api_token)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    print("Webhook и pending updates сброшены")


if __name__ == "__main__":
    asyncio.run(main())
