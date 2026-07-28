"""
Messages: kurs bo'yicha chat ajratilishi tarixi va broadcast scope testlari.
"""
import uuid
import pytest
from httpx import AsyncClient

from conftest import TestingSessionLocal
from messages.models import Message
from messages.router import ConnectionManager


class FakeWebSocket:
    """ConnectionManager testlari uchun soxta WebSocket."""

    def __init__(self):
        self.sent = []

    async def accept(self):
        pass

    async def send_json(self, data):
        self.sent.append(data)


@pytest.mark.asyncio
async def test_broadcast_scoped_by_course_id():
    """Xabar faqat bir xil school_id VA bir xil course_id dagi ulanishlarga boradi."""
    manager = ConnectionManager()
    school_id = uuid.uuid4()
    course_a, course_b = str(uuid.uuid4()), str(uuid.uuid4())

    ws_global = FakeWebSocket()
    ws_course_a = FakeWebSocket()
    ws_course_b = FakeWebSocket()
    await manager.connect(ws_global, school_id, "Global User", None)
    await manager.connect(ws_course_a, school_id, "User A", course_a)
    await manager.connect(ws_course_b, school_id, "User B", course_b)

    await manager.broadcast(school_id, "kurs A xabari", sender="User A", course_id=course_a)
    assert [m["text"] for m in ws_course_a.sent] == ["kurs A xabari"]
    assert ws_course_b.sent == []
    assert ws_global.sent == []

    await manager.broadcast(school_id, "global xabar", sender="Global User", course_id=None)
    assert [m["text"] for m in ws_global.sent] == ["global xabar"]
    assert [m["text"] for m in ws_course_a.sent] == ["kurs A xabari"]
    assert ws_course_b.sent == []

    manager.disconnect(ws_course_a)
    await manager.broadcast(school_id, "yana kurs A", sender="User A", course_id=course_a)
    assert [m["text"] for m in ws_course_a.sent] == ["kurs A xabari"]


@pytest.mark.asyncio
async def test_history_scoped_by_course(client: AsyncClient, admin_auth):
    """GET /history: course_id berilsa kurs xabarlari, berilmasa faqat global (course_id IS NULL)."""
    school_id = admin_auth["school_id"]
    user_id = admin_auth["user_id"]
    course_id = uuid.uuid4()

    async with TestingSessionLocal() as session:
        session.add(Message(content="global xabar", sender_id=user_id, school_id=school_id, course_id=None))
        session.add(Message(content="kurs xabari", sender_id=user_id, school_id=school_id, course_id=course_id))
        await session.commit()

    headers = admin_auth["headers"]

    res = await client.get(f"/api/v1/messages/history?course_id={course_id}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert [m["content"] for m in data] == ["kurs xabari"]
    assert data[0]["sender"] == "Test Admin"

    res = await client.get("/api/v1/messages/history", headers=headers)
    assert res.status_code == 200
    assert [m["content"] for m in res.json()] == ["global xabar"]
