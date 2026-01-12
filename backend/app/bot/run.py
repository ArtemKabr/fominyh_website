# backend/app/bot/run.py — запуск Telegram-бота

import asyncio
from app.bot.dispatcher import dp, bot


async def run_bot() -> None:
    """Запуск Telegram-бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
