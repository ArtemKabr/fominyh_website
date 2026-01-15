# backend/tests/test_booking_create.py — создание записи
# Назначение: создание записи через day + time (как в проекте)

from datetime import datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_create_booking_ok(client):
    dt = datetime.now() + timedelta(hours=1)  # (я изменил)

    r = await client.post(
        "/api/booking",
        json={
            "service_id": 1,
            "day": dt.date().isoformat(),  # (я изменил)
            "time": dt.strftime("%H:%M"),  # (я изменил)
            "user_name": "Ivan",
            "phone": "+79991111111",
            "email": "ivan@test.ru",
        },
    )
    assert r.status_code == 201
    assert r.json()["service_id"] == 1


@pytest.mark.asyncio
async def test_create_booking_overlap(client):
    dt = datetime.now() + timedelta(hours=1)  # (я изменил)

    await client.post(
        "/api/booking",
        json={
            "service_id": 1,
            "day": dt.date().isoformat(),  # (я изменил)
            "time": dt.strftime("%H:%M"),  # (я изменил)
            "user_name": "Ivan",
            "phone": "+79992222222",
            "email": "ivan2@test.ru",
        },
    )

    r = await client.post(
        "/api/booking",
        json={
            "service_id": 1,
            "day": dt.date().isoformat(),  # (я изменил)
            "time": dt.strftime("%H:%M"),  # (я изменил)
            "user_name": "Petr",
            "phone": "+79993333333",
            "email": "petr@test.ru",
        },
    )
    assert r.status_code == 409
