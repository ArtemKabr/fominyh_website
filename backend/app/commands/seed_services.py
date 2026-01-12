# backend/app/commands/seed_services.py — наполнение БД услугами

import asyncio

from app.core.database import async_session_maker
from app.models.service import Service


SERVICES = [
    {
        "name": "Скульптинг лица",
        "slug": "face-sculpting",
        "description": "Глубокая моделирующая техника для мышц лица.",
        "duration_minutes": 60,
        "price": 3000,
    },
    {
        "name": "Массаж Гуаша",
        "slug": "gua-sha",
        "description": "Лимфодренаж и снятие отёков.",
        "duration_minutes": 45,
        "price": 2500,
    },
    {
        "name": "Биоэнергетический массаж",
        "slug": "bio-energy",
        "description": "Глубокая работа с телом и восстановление баланса.",
        "duration_minutes": 90,
        "price": 5000,
    },
]


async def main():
    async with async_session_maker() as db:
        for data in SERVICES:
            exists = await db.scalar(
                Service.__table__.select().where(Service.slug == data["slug"])
            )
            if exists:
                continue

            db.add(Service(**data))

        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
