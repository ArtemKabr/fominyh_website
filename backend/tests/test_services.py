# backend/tests/test_services.py — тесты услуг

import pytest


@pytest.mark.asyncio
async def test_get_services(client):
    """Получение списка услуг."""

    response = await client.get("/api/services")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
