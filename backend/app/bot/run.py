# backend/app/bot/run.py — запуск Telegram-бота

import asyncio
from app.bot.bot import get_bot, get_dispatcher
from app.bot.handlers import user_start, user_phone, admin_confirm  # (я добавил)


async def main():
    bot = get_bot()
    dp = get_dispatcher()

    if not bot or not dp:
        return

    dp.include_router(user_start.router)   # (я добавил)
    dp.include_router(user_phone.router)   # (я добавил)
    dp.include_router(admin_confirm.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
