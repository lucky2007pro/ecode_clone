"""
Users & Auth Unit and Integration Tests.
"""
import pytest
from httpx import AsyncClient

from conftest import TEST_OTP_CODE

ADMIN_PAYLOAD = {
    "email": "new_owner@exode.biz",
    "password": "securepassword123",
    "full_name": "Alisher Navoiy",
    "role": "admin",
    "school_name": "Navoiy School",
    "subdomain": "navoiy-school",
}


@pytest.mark.asyncio
async def test_user_registration_success(client: AsyncClient, otp_redis):
    """OTP oqimi orqali admin (maktab egasi) muvaffaqiyatli ro'yxatdan o'tishi."""
    send_res = await client.post("/api/v1/users/register/send-otp", json=ADMIN_PAYLOAD)
    assert send_res.status_code == 200

    verify_res = await client.post(
        "/api/v1/users/register/verify",
        json={**ADMIN_PAYLOAD, "otp_code": TEST_OTP_CODE},
    )
    assert verify_res.status_code == 201
    data = verify_res.json()
    assert data["email"] == "new_owner@exode.biz"
    assert data["role"] == "admin"
    assert "id" in data


@pytest.mark.asyncio
async def test_user_registration_duplicate_email(client: AsyncClient, otp_redis):
    """Bir xil email bilan qayta ro'yxatdan o'tishni rad etish."""
    payload = {**ADMIN_PAYLOAD, "email": "duplicate@exode.biz", "subdomain": "dup-school"}

    # Birinchi marta to'liq ro'yxatdan o'tish (OTP tasdiqlash bilan)
    res1 = await client.post("/api/v1/users/register/send-otp", json=payload)
    assert res1.status_code == 200
    res_verify = await client.post(
        "/api/v1/users/register/verify",
        json={**payload, "otp_code": TEST_OTP_CODE},
    )
    assert res_verify.status_code == 201

    # Ikkinchi marta bir xil email bilan urinish
    res2 = await client.post("/api/v1/users/register/send-otp", json=payload)
    assert res2.status_code == 400
    assert "allaqachon mavjud" in res2.json()["detail"]
