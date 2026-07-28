"""
Payments: tariflar, obuna sotib olish, balans to'ldirish, kurs purchase testlari.
"""
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from conftest import TestingSessionLocal
from users.models import User
from users.auth import hash_password, create_access_token
from schools.models import UserSchool, MembershipStatus
from payments.models import SchoolSubscription, SubscriptionStatus
from permissions.enums import Role


async def _set_balance(user_id, amount: float):
    async with TestingSessionLocal() as session:
        user = await session.get(User, user_id)
        user.balance = amount
        await session.commit()


async def _get_balance(user_id) -> float:
    async with TestingSessionLocal() as session:
        user = await session.get(User, user_id)
        return float(user.balance)


async def _make_student(admin_auth):
    async with TestingSessionLocal() as session:
        student = User(
            email="student@pay.com",
            full_name="Pay Student",
            hashed_password=hash_password("password123"),
            role=Role.STUDENT,
        )
        session.add(student)
        await session.flush()
        session.add(UserSchool(user_id=student.id, school_id=admin_auth["school_id"], status=MembershipStatus.APPROVED))
        await session.commit()
        student_id = student.id
    token = create_access_token(user_id=str(student_id), role=Role.STUDENT.value, school_id=str(admin_auth["school_id"]))
    return {"headers": {"Authorization": f"Bearer {token}"}, "user_id": student_id}


@pytest.mark.asyncio
async def test_plans_returns_three_tariffs(client: AsyncClient):
    res = await client.get("/api/v1/payments/plans")
    assert res.status_code == 200
    plans = res.json()
    assert len(plans) == 3
    assert {p["name"] for p in plans} == {"Boshlang'ich", "Standart", "Premium"}


@pytest.mark.asyncio
async def test_subscribe_deducts_balance_and_creates_subscription(client: AsyncClient, admin_auth):
    await _set_balance(admin_auth["user_id"], 1_000_000)

    res = await client.post("/api/v1/payments/subscribe", json={"plan_id": "standard"}, headers=admin_auth["headers"])
    assert res.status_code == 200
    data = res.json()
    assert data["plan_name"] == "Standart"
    assert data["status"] == "active"
    assert "expires_at" in data

    assert await _get_balance(admin_auth["user_id"]) == 700_000

    # Obuna GET orqali ham ko'rinadi
    sub_res = await client.get("/api/v1/payments/school-subscription", headers=admin_auth["headers"])
    assert sub_res.status_code == 200
    assert sub_res.json()["plan_name"] == "Standart"

    # Tranzaksiya yozilgan
    tx_res = await client.get("/api/v1/payments/transactions/me", headers=admin_auth["headers"])
    txs = tx_res.json()
    assert txs[0]["type"] == "out"
    assert txs[0]["amount"] == 300_000
    assert "Standart" in txs[0]["description"]

    # Eski obuna bekor bo'ladi — qayta obuna bo'lganda bittasi ACTIVE qoladi
    await client.post("/api/v1/payments/subscribe", json={"plan_id": "starter"}, headers=admin_auth["headers"])
    async with TestingSessionLocal() as session:
        result = await session.execute(
            select(SchoolSubscription).where(
                SchoolSubscription.school_id == admin_auth["school_id"],
                SchoolSubscription.status == SubscriptionStatus.ACTIVE,
            )
        )
        assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_subscribe_insufficient_balance(client: AsyncClient, admin_auth):
    await _set_balance(admin_auth["user_id"], 100)
    res = await client.post("/api/v1/payments/subscribe", json={"plan_id": "premium"}, headers=admin_auth["headers"])
    assert res.status_code == 400
    assert await _get_balance(admin_auth["user_id"]) == 100


@pytest.mark.asyncio
async def test_topup_increases_balance_and_notifies(client: AsyncClient, admin_auth):
    student = await _make_student(admin_auth)

    res = await client.post("/api/v1/payments/topup", json={
        "user_id": str(student["user_id"]), "amount": 50_000, "description": "Sinov to'lovi",
    }, headers=admin_auth["headers"])
    assert res.status_code == 201
    assert res.json()["type"] == "in"
    assert await _get_balance(student["user_id"]) == 50_000

    # Foydalanuvchiga bildirishnoma tushgan
    notif_res = await client.get("/api/v1/notifications/", headers=student["headers"])
    titles = [n["title"] for n in notif_res.json()["results"]]
    assert "Balans to'ldirildi" in titles


@pytest.mark.asyncio
async def test_student_cannot_subscribe_or_topup(client: AsyncClient, admin_auth):
    student = await _make_student(admin_auth)

    sub = await client.post("/api/v1/payments/subscribe", json={"plan_id": "starter"}, headers=student["headers"])
    assert sub.status_code == 403

    top = await client.post("/api/v1/payments/topup", json={
        "user_id": str(student["user_id"]), "amount": 1000,
    }, headers=student["headers"])
    assert top.status_code == 403


async def _make_course(client: AsyncClient, admin_auth, price: float, title: str = "Test kurs") -> str:
    slug = f"purchase-test-{uuid.uuid4().hex[:8]}"
    res = await client.post(
        "/api/v1/courses/",
        json={"title": title, "slug": slug, "price": price},
        headers=admin_auth["headers"],
    )
    assert res.status_code == 201, res.text
    return res.json()["id"]


@pytest.mark.asyncio
async def test_purchase_deducts_balance_and_creates_enrollment_tx_notification(client: AsyncClient, admin_auth):
    student = await _make_student(admin_auth)
    await _set_balance(student["user_id"], 50_000)
    course_id = await _make_course(client, admin_auth, 30_000)

    res = await client.post("/api/v1/enrollments/purchase", json={"course_id": course_id}, headers=student["headers"])
    assert res.status_code == 201, res.text
    assert res.json()["course_id"] == course_id

    # Balans kamaydi
    assert await _get_balance(student["user_id"]) == 20_000

    # OUT tranzaksiya yozilgan
    tx_res = await client.get("/api/v1/payments/transactions/me", headers=student["headers"])
    txs = tx_res.json()
    assert len(txs) == 1
    assert txs[0]["type"] == "out"
    assert float(txs[0]["amount"]) == 30_000
    assert "Kurs sotib olindi" in txs[0]["description"]

    # O'quvchiga va adminlarga bildirishnoma tushgan
    s_notif = await client.get("/api/v1/notifications/", headers=student["headers"])
    assert "Kurs sotib olindi" in [n["title"] for n in s_notif.json()["results"]]
    a_notif = await client.get("/api/v1/notifications/", headers=admin_auth["headers"])
    assert "Kurs sotib olindi" in [n["title"] for n in a_notif.json()["results"]]


@pytest.mark.asyncio
async def test_purchase_free_course_keeps_balance(client: AsyncClient, admin_auth):
    student = await _make_student(admin_auth)
    course_id = await _make_course(client, admin_auth, 0)

    res = await client.post("/api/v1/enrollments/purchase", json={"course_id": course_id}, headers=student["headers"])
    assert res.status_code == 201, res.text

    assert await _get_balance(student["user_id"]) == 0
    tx_res = await client.get("/api/v1/payments/transactions/me", headers=student["headers"])
    assert tx_res.json() == []


@pytest.mark.asyncio
async def test_purchase_insufficient_balance(client: AsyncClient, admin_auth):
    student = await _make_student(admin_auth)
    await _set_balance(student["user_id"], 10_000)
    course_id = await _make_course(client, admin_auth, 30_000)

    res = await client.post("/api/v1/enrollments/purchase", json={"course_id": course_id}, headers=student["headers"])
    assert res.status_code == 400
    assert "yetarli emas" in res.json()["detail"]

    # Balans o'zgarmagan, enrollment yaratilmagan
    assert await _get_balance(student["user_id"]) == 10_000
    enr = await client.get(f"/api/v1/enrollments/user/{student['user_id']}", headers=admin_auth["headers"])
    assert enr.json() == []


@pytest.mark.asyncio
async def test_purchase_duplicate_rejected(client: AsyncClient, admin_auth):
    student = await _make_student(admin_auth)
    await _set_balance(student["user_id"], 100_000)
    course_id = await _make_course(client, admin_auth, 30_000)

    first = await client.post("/api/v1/enrollments/purchase", json={"course_id": course_id}, headers=student["headers"])
    assert first.status_code == 201

    second = await client.post("/api/v1/enrollments/purchase", json={"course_id": course_id}, headers=student["headers"])
    assert second.status_code == 400
    assert await _get_balance(student["user_id"]) == 70_000


@pytest.mark.asyncio
async def test_admin_cannot_use_purchase_endpoint(client: AsyncClient, admin_auth):
    course_id = await _make_course(client, admin_auth, 30_000)
    res = await client.post("/api/v1/enrollments/purchase", json={"course_id": course_id}, headers=admin_auth["headers"])
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_purchase_course_not_found(client: AsyncClient, admin_auth):
    student = await _make_student(admin_auth)
    res = await client.post(
        "/api/v1/enrollments/purchase",
        json={"course_id": str(uuid.uuid4())},
        headers=student["headers"],
    )
    assert res.status_code == 404
