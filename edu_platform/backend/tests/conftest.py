"""
Pytest Fixtures for FastAPI Async Testing with AsyncClient & SQLite in-memory DB.
"""
import os

# Test muhitini db/main import qilishdan OLDIN sozlash (zaruriy env o'zgaruvchilar)
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from db import Base, get_db
from main import app
from users.models import User
from users.auth import hash_password, create_access_token
from schools.models import School, UserSchool, MembershipStatus
from permissions.enums import Role

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DB_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


TEST_OTP_CODE = "123456"


class FakeRedis:
    """Redis o'rniga xotirada ishlaydigan oddiy stub (testlar uchun)."""

    def __init__(self):
        self._store: dict = {}

    async def setex(self, key, ttl, value):
        self._store[key] = value

    async def get(self, key):
        return self._store.get(key)

    async def delete(self, *keys):
        for key in keys:
            self._store.pop(key, None)


@pytest.fixture
def otp_redis(monkeypatch):
    """Email OTP yuborish va Redis'ni test stub'lari bilan almashtiradi."""
    fake = FakeRedis()

    async def fake_send_email_otp(email: str) -> str:
        return TEST_OTP_CODE

    async def fake_get_redis():
        return fake

    monkeypatch.setattr("users.router.send_email_otp", fake_send_email_otp)
    monkeypatch.setattr("users.router.get_redis", fake_get_redis)
    return fake


@pytest.fixture
async def db_user() -> User:
    """Ma'lumotlar bazasida yaratilgan oddiy foydalanuvchi (login qilinmagan)."""
    async with TestingSessionLocal() as session:
        user = User(
            email="owner@test.com",
            full_name="School Owner",
            hashed_password=hash_password("password123"),
            role=Role.ADMIN,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest.fixture
async def admin_auth() -> dict:
    """Tasdiqlangan admin + maktab yaratib, Bearer sarlavhasini qaytaradi."""
    async with TestingSessionLocal() as session:
        user = User(
            email="admin@test.com",
            full_name="Test Admin",
            hashed_password=hash_password("password123"),
            role=Role.ADMIN,
        )
        session.add(user)
        await session.flush()
        school = School(name="Test School", subdomain="test-school", owner_id=user.id)
        session.add(school)
        await session.flush()
        session.add(UserSchool(user_id=user.id, school_id=school.id, status=MembershipStatus.APPROVED))
        await session.commit()
        user_id, school_id = user.id, school.id
    token = create_access_token(user_id=str(user_id), role=Role.ADMIN.value, school_id=str(school_id))
    return {"headers": {"Authorization": f"Bearer {token}"}, "user_id": user_id, "school_id": school_id}
