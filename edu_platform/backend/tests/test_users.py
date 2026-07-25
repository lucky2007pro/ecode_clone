"""
Users & Auth Unit and Integration Tests.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_registration_success(client: AsyncClient):
    """Yangi foydalanuvchi muvaffaqiyatli ro'yxatdan o'tishi."""
    payload = {
        "email": "new_teacher@exode.biz",
        "password": "securepassword123",
        "full_name": "Alisher Navoiy",
        "role": "expert_teacher"
    }
    response = await client.post("/api/v1/users/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new_teacher@exode.biz"
    assert data["role"] == "expert_teacher"
    assert "id" in data


@pytest.mark.asyncio
async def test_user_registration_duplicate_email(client: AsyncClient):
    """Bir xil email bilan qayta ro'yxatdan o'tishni rad etish."""
    payload = {
        "email": "duplicate@exode.biz",
        "password": "password123",
        "full_name": "Test User",
        "role": "school_owner"
    }
    # Birinchi marta ro'yxatdan o'tish
    res1 = await client.post("/api/v1/users/register", json=payload)
    assert res1.status_code == 201

    # Ikkinchi marta bir xil email bilan urinish
    res2 = await client.post("/api/v1/users/register", json=payload)
    assert res2.status_code == 400
    assert "allaqachon mavjud" in res2.json()["detail"]
