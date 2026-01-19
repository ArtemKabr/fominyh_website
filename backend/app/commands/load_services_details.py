# backend/app/commands/load_services_details.py
# Назначение: загрузка описаний процедур в таблицу services
# запуск
# docker compose exec backend python app/commands/load_services_details.py
import asyncio

from sqlalchemy import select
from app.db.session import async_session
from app.models.service import Service
from app.data.services_details import SERVICES_DETAILS


async def load_services_details() -> None:
    async with async_session() as session:
        for slug, data in SERVICES_DETAILS.items():
            result = await session.execute(
                select(Service).where(Service.slug == slug)
            )
            service = result.scalar_one_or_none()

            if not service:
                continue

            service.description = data["how_it_works"]
            service.benefits = data["benefits"]

        await session.commit()


if __name__ == "__main__":
    asyncio.run(load_services_details())
