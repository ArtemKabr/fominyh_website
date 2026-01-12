# backend/tests/test_booking_create.py — создание записи
from datetime import datetime, timedelta
import pytest


@pytest.mark.asyncio
async def test_create_booking_ok(client):
    start = (datetime.now() + timedelta(hours=1)).isoformat()

    r = await client.post(
        "/api/booking",
        json={
            "service_id": 1,
            "start_time": start,
            "user_name": "Ivan",
            "phone": "+79991111111",
            "email": "ivan@test.ru",
        },
    )
    assert r.status_code == 201
    assert r.json()["service_id"] == 1


@pytest.mark.asyncio
async def test_create_booking_overlap(client):
    start = (datetime.now() + timedelta(hours=1)).isoformat()

    await client.post(
        "/api/booking",
        json={
            "service_id": 1,
            "start_time": start,
            "user_name": "Ivan",
            "phone": "+79992222222",
            "email": "ivan2@test.ru",
        },
    )

    r = await client.post(
        "/api/booking",
        json={
            "service_id": 1,
            "start_time": start,
            "user_name": "Petr",
            "phone": "+79993333333",
            "email": "petr@test.ru",
        },
    )
    assert r.status_code == 409
