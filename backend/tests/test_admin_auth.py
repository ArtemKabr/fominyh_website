# backend/tests/test_admin_auth.py — тесты упрощённой авторизации

import pytest


@pytest.mark.asyncio
async def test_register_ok(client):
    r = await client.post(
        "/api/auth/register",
        json={
            "name": "Test",
            "phone": "+79990000000",
            "email": "test@test.ru",
            "password": "12345678",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data["email"] == "test@test.ru"


@pytest.mark.asyncio
async def test_login_ok(client):
    r = await client.post(
        "/api/auth/login",
        json={
            "email": "test@test.ru",
            "password": "12345678",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "test@test.ru"
    assert data["is_admin"] is False
