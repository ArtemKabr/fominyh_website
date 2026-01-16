# backend/app/bot/handlers/user_menu.py
# Назначение: показ меню и обработка кнопок пользователя

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.keyboards.user import user_main_menu_kb

router = Router()


@router.callback_query(F.data == "user:menu")
async def user_menu(callback: CallbackQuery) -> None:
    """Показ главного меню пользователя."""  # (я добавил)
    text = "Выберите действие:"

    if callback.message.text != text:  # (я добавил)
        await callback.message.edit_text(
            text,
            reply_markup=user_main_menu_kb(),
        )

    await callback.answer()
