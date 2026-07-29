"""
Enrollments: kurs talabalari ro'yxatida full_name qaytarilishi testlari.
"""

import uuid

import pytest

from httpx import AsyncClient

from conftest import TestingSessionLocal

from users.models import User

from users.auth import hash_password

from permissions.enums import Role

async def _create_course(client: AsyncClient, headers) -> str:

    suffix = uuid.uuid4().hex[:8]

    res = await client.post("/api/v1/courses/", json={

        "title": "Enrollment Course", "slug": f"enroll-course-{suffix}",

        "description": "Enrollment testlari uchun kurs", "price": 5000.0,

    }, headers=headers)

    assert res.status_code == 201

    return res.json()["id"]

async def _create_student(email: str, full_name: str) -> uuid.UUID:

    async with TestingSessionLocal() as session:

        student = User(

            email=email,

            full_name=full_name,

            hashed_password=hash_password("password123"),

            role=Role.STUDENT,

        )

        session.add(student)

        await session.commit()

        await session.refresh(student)

        return student.id

@pytest.mark.asyncio

async def test_course_enrollments_include_full_name(client: AsyncClient, admin_auth):

    """GET /enrollments/course/{id} javobida talabaning full_name'i bo'ladi."""

    headers = admin_auth["headers"]

    course_id = await _create_course(client, headers)

    student_id = await _create_student("student1@test.com", "Ali Valiyev")

    enroll = await client.post("/api/v1/enrollments/", json={

        "user_id": str(student_id), "course_id": course_id,

    }, headers=headers)

    assert enroll.status_code == 201

    res = await client.get(f"/api/v1/enrollments/course/{course_id}", headers=headers)

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1

    assert data[0]["user_id"] == str(student_id)

    assert data[0]["full_name"] == "Ali Valiyev"

    assert data[0]["role"] == "student"

@pytest.mark.asyncio

async def test_user_enrollments_response_unchanged(client: AsyncClient, admin_auth):

    """GET /enrollments/user/{id} eski maydonlar bilan ishlayveradi (backward-compat)."""

    headers = admin_auth["headers"]

    course_id = await _create_course(client, headers)

    student_id = await _create_student("student2@test.com", "Vali Aliyev")

    enroll = await client.post("/api/v1/enrollments/", json={

        "user_id": str(student_id), "course_id": course_id,

    }, headers=headers)

    assert enroll.status_code == 201

    res = await client.get(f"/api/v1/enrollments/user/{student_id}", headers=headers)

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1

    assert data[0]["course_id"] == course_id

    assert "status" in data[0] and "progress" in data[0]

