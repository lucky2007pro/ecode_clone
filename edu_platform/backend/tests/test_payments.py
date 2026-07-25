"""
Payments & Installments Unit and Integration Tests.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_payments(client: AsyncClient):
    """To'lovlar ro'yxatini olish testi."""
    res = await client.get("/api/v1/payments/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["provider"] == "payme"
