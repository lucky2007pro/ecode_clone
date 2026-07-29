"""
Schools Multi-tenant Unit and Integration Tests.
"""

import pytest

from httpx import AsyncClient

@pytest.mark.asyncio

async def test_create_school(client: AsyncClient, db_user):

    """Multi-tenant maktab yaratish (owner_id query param sifatida yuboriladi)."""

    payload = {

        "name": "Najot Ta'lim Online",

        "subdomain": "najot-edu",

    }

    res = await client.post("/api/v1/schools/", json=payload, params={"owner_id": str(db_user.id)})

    assert res.status_code == 201

    data = res.json()

    assert data["subdomain"] == "najot-edu"

    assert data["primary_color"] == "#6366f1"

    assert data["is_active"] is True

