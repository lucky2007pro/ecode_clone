"""
Notifications: event orqali yaratilish, scope va o'qilganini belgilash testlari.
"""

import uuid

import pytest

from httpx import AsyncClient

from conftest import TestingSessionLocal

from users.models import User

from users.auth import hash_password, create_access_token

from schools.models import UserSchool, MembershipStatus

from permissions.enums import Role

async def _make_teacher(admin_auth):

    """Maktabga tasdiqlangan teacher qo'shib ekanmiz."""

    suffix = uuid.uuid4().hex[:8]

    async with TestingSessionLocal() as session:

        teacher = User(

            email=f"teacher-{suffix}@test.com",

            full_name="Test Teacher",

            hashed_password=hash_password("password123"),

            role=Role.TEACHER,

        )

        session.add(teacher)

        await session.flush()

        session.add(UserSchool(user_id=teacher.id, school_id=admin_auth["school_id"], status=MembershipStatus.APPROVED))

        await session.commit()

        teacher_id = teacher.id

    token = create_access_token(user_id=str(teacher_id), role=Role.TEACHER.value, school_id=str(admin_auth["school_id"]))

    return {"headers": {"Authorization": f"Bearer {token}"}, "user_id": teacher_id}

async def _submit_homework(client: AsyncClient, admin_auth, teacher):

    """Teacher kurs+dars yaratadi, so'ng uy vazifasi yuboriladi (teacher event ini ishga tushiradi)."""

    suffix = uuid.uuid4().hex[:8]

    course = await client.post("/api/v1/courses/", json={

        "title": "Notif Course", "slug": f"notif-course-{suffix}",

        "description": "Bildirishnoma testlari uchun kurs", "price": 1000.0,

    }, headers=teacher["headers"])

    assert course.status_code == 201

    lesson = await client.post("/api/v1/lessons/", json={

        "course_id": course.json()["id"], "title": "Dars 1", "lesson_type": "video", "order": 0,

    }, headers=teacher["headers"])

    assert lesson.status_code == 201

    homework = await client.post("/api/v1/homeworks/", json={

        "lesson_id": lesson.json()["id"],

        "student_id": str(admin_auth["user_id"]),

        "submission_text": "Vazifa bajarildi",

    }, headers=admin_auth["headers"])

    assert homework.status_code == 201

    return homework.json()["id"]

@pytest.mark.asyncio

async def test_homework_submit_notifies_teacher_not_admin(client: AsyncClient, admin_auth):

    """Uy vazifasi yuborilganda faqat kurs teacher'iga tushadi, adminga tushmaydi."""

    teacher = await _make_teacher(admin_auth)

    await _submit_homework(client, admin_auth, teacher)

    res = await client.get("/api/v1/notifications/", headers=teacher["headers"])

    assert res.status_code == 200

    data = res.json()

    assert data["unread_count"] == 1

    assert data["results"][0]["title"] == "Yangi uy vazifasi yuborildi"

    assert data["results"][0]["is_read"] is False

    admin_notes = (await client.get("/api/v1/notifications/", headers=admin_auth["headers"])).json()

    assert admin_notes == {"unread_count": 0, "results": []}

@pytest.mark.asyncio

async def test_mark_read_and_read_all(client: AsyncClient, admin_auth):

    """Bitta bildirishnomani va hammasini o'qilgan deb belgilash."""

    teacher = await _make_teacher(admin_auth)

    await _submit_homework(client, admin_auth, teacher)

    headers = teacher["headers"]

    listing = (await client.get("/api/v1/notifications/", headers=headers)).json()

    note_id = listing["results"][0]["id"]

    read = await client.post(f"/api/v1/notifications/{note_id}/read", headers=headers)

    assert read.status_code == 200

    assert read.json()["is_read"] is True

    after = (await client.get("/api/v1/notifications/", headers=headers)).json()

    assert after["unread_count"] == 0

    await _submit_homework(client, admin_auth, teacher)

    res = await client.post("/api/v1/notifications/read-all", headers=headers)

    assert res.status_code == 204

    final = (await client.get("/api/v1/notifications/", headers=headers)).json()

    assert final["unread_count"] == 0

@pytest.mark.asyncio

async def test_read_unknown_notification_returns_404(client: AsyncClient, admin_auth):

    random_id = "00000000-0000-0000-0000-000000000001"

    res = await client.post(f"/api/v1/notifications/{random_id}/read", headers=admin_auth["headers"])

    assert res.status_code == 404

@pytest.mark.asyncio

async def test_notifications_scoped_to_owner(client: AsyncClient, admin_auth):

    """Boshqa foydalanuvchi teacher bildirishnomalarini ko'ra olmaydi."""

    teacher = await _make_teacher(admin_auth)

    await _submit_homework(client, admin_auth, teacher)

    async with TestingSessionLocal() as session:

        outsider = User(

            email="outsider@test.com",

            full_name="Out Sider",

            hashed_password=hash_password("password123"),

            role=Role.ADMIN,

        )

        session.add(outsider)

        await session.commit()

        await session.refresh(outsider)

        token = create_access_token(user_id=str(outsider.id), role=outsider.role.value, school_id="")

    res = await client.get("/api/v1/notifications/", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200

    assert res.json() == {"unread_count": 0, "results": []}

