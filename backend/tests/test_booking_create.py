# backend/tests/test_booking_create.py — тест создания записи (API)
import pytest


@pytest.mark.asyncio
async def test_create_booking(client, monkeypatch):
    """Создание записи через API."""  # (я добавил)

    async def fake_create_booking(*, db, booking_in):
        return {
            "id": 1,
            "user_id": 1,  # обязателен для BookingRead  # (я добавил)
            "service_id": booking_in.service_id,
            "start_time": booking_in.start_time,
        }

    # мокаем сервисный слой  # (я добавил)
    monkeypatch.setattr(
        "app.api.booking.create_booking",
        fake_create_booking,
    )

    payload = {
        "service_id": 1,
        "start_time": "2025-01-10T12:00:00",
        "user_name": "Иван",
        "phone": "+79990000000",
        "email": "test@mail.ru",
    }

    response = await client.post("/api/booking", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["service_id"] == 1
