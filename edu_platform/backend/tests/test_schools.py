"""
Schools Multi-tenant Unit and Integration Tests.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_school(client: AsyncClient):
    """Multi-tenant maktab yaratish va brending sozlash."""
    payload = {
        "name": "Najot Ta'lim Online",
        "subdomain": "najot-edu",
        "primary_color": "#4f46e5"
    }
    res = await client.post("/api/v1/schools/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["subdomain"] == "najot-edu"
    assert data["primary_color"] == "#4f46e5"
    assert data["is_active"] is True
