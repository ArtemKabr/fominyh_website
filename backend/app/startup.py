# backend/app/startup.py — автоматическая инициализация данных
# Назначение: автозагрузка услуг при первом запуске

from sqlalchemy import select, text
from sqlalchemy.exc import ProgrammingError

from app.models.service import Service
from app.commands.load_services import load_services
from app.core.database import get_async_session


async def init_services_if_empty() -> None:
    """Загрузить услуги, если таблица существует и пуста."""  #

    async for db in get_async_session():
        try:
            # проверяем, что таблица services существует  #
            await db.execute(text("SELECT 1 FROM services LIMIT 1"))
        except ProgrammingError:
            # таблицы ещё нет — alembic не отработал  #
            return

        result = await db.execute(select(Service.id).limit(1))
        exists = result.scalar_one_or_none()

        if exists:
            return

        await load_services(db)  #
