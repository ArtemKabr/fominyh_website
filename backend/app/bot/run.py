# backend/app/bot/run.py — запуск Telegram-бота
# Назначение: точка входа

import asyncio

from app.bot.bot import bot, dp
from app.bot.dispatcher import setup_dispatcher


async def main() -> None:
    """Запуск бота."""  # (я добавил)

    setup_dispatcher(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
