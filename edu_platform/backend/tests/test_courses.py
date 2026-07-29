"""
Courses & Homework Unit and Integration Tests.
"""

import pytest

from httpx import AsyncClient

@pytest.mark.asyncio

async def test_create_course(client: AsyncClient, admin_auth):

    """Yangi kurs yaratish testi (MANAGE_COURSES ruxsati bilan)."""

    payload = {

        "title": "FastAPI & Microservices Architecture",

        "slug": "fastapi-architecture",

        "description": "Python asinxron mikroservislar arxitekturasi",

        "price": 1500000.0

    }

    res = await client.post("/api/v1/courses/", json=payload, headers=admin_auth["headers"])

    assert res.status_code == 201

    data = res.json()

    assert data["title"] == "FastAPI & Microservices Architecture"

    assert data["slug"] == "fastapi-architecture"

    assert data["price"] == 1500000.0

