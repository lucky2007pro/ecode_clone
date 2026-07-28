import uuid
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db, AsyncSessionLocal
from messages.models import Message
from schools.models import UserSchool, MembershipStatus
from users.auth import SECRET_KEY, ALGORITHM
from permissions.dependencies import get_current_school_id

router = APIRouter()


class ConnectionManager:
    """Maktab va kurs bo'yicha ajratilgan WebSocket ulanishlari (multi-tenant)."""

    def __init__(self):
        # Har biri: (websocket, school_id, sender_name, course_id)
        self.active_connections: list[tuple[WebSocket, uuid.UUID, str, str | None]] = []

    async def connect(self, websocket: WebSocket, school_id: uuid.UUID, sender_name: str, course_id: str | None):
        await websocket.accept()
        self.active_connections.append((websocket, school_id, sender_name, course_id))

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [c for c in self.active_connections if c[0] is not websocket]

    async def broadcast(self, school_id: uuid.UUID, text: str, sender: str, course_id: str | None):
        """Faqat shu maktab va shu chat (kurs yoki global) dagi ulanishlarga xabar tarqatish."""
        for connection, conn_school_id, _, conn_course_id in self.active_connections:
            if conn_school_id == school_id and conn_course_id == course_id:
                await connection.send_json({"sender": sender, "text": text})


manager = ConnectionManager()

POLICY_VIOLATION = 1008


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, course_id: str | None = None):
    # 1. Tokenni query paramdan olish va tekshirish
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=POLICY_VIOLATION)
        return
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError("No sub")
        user_uuid = uuid.UUID(user_id)
    except (JWTError, ValueError):
        await websocket.close(code=POLICY_VIOLATION)
        return

    # 2. Foydalanuvchi va tasdiqlangan a'zoligini bazadan topish
    from users.models import User
    from courses.models import Course
    from enrollments.models import Enrollment

    course_uuid = None
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(select(User).where(User.id == user_uuid))
        user = user_res.scalar_one_or_none()
        if not user:
            await websocket.close(code=POLICY_VIOLATION)
            return
        membership_res = await session.execute(
            select(UserSchool)
            .where(UserSchool.user_id == user.id)
            .where(UserSchool.status == MembershipStatus.APPROVED)
        )
        membership = membership_res.scalars().first()
        if not membership:
            await websocket.close(code=POLICY_VIOLATION)
            return

        school_id = membership.school_id

        # 3. Kurs chati bo'lsa: kurs shu maktabda borligini va student yozilganligini tekshirish
        if course_id:
            try:
                course_uuid = uuid.UUID(course_id)
            except ValueError:
                await websocket.close(code=POLICY_VIOLATION)
                return
            course_res = await session.execute(
                select(Course)
                .where(Course.id == course_uuid)
                .where(Course.school_id == school_id)
            )
            if not course_res.scalar_one_or_none():
                await websocket.close(code=POLICY_VIOLATION)
                return
            if payload.get("role") == "student":
                enrollment_res = await session.execute(
                    select(Enrollment)
                    .where(Enrollment.user_id == user.id)
                    .where(Enrollment.course_id == course_uuid)
                )
                if not enrollment_res.scalar_one_or_none():
                    await websocket.close(code=POLICY_VIOLATION)
                    return

    sender_name = user.full_name or user.email

    await manager.connect(websocket, school_id, sender_name, course_id)
    try:
        while True:
            data = await websocket.receive_text()

            # Xabarni mustaqil sessiya orqali bazaga saqlash
            async with AsyncSessionLocal() as session:
                session.add(Message(content=data, sender_id=user.id, school_id=school_id, course_id=course_uuid))
                await session.commit()

            # Faqat shu maktabning shu chat a'zolariga tarqatamiz
            await manager.broadcast(school_id, data, sender=sender_name, course_id=course_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(school_id, "Foydalanuvchi chatdan chiqdi", sender="System", course_id=course_id)


@router.get("/history")
async def get_chat_history(
    course_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
    school_id=Depends(get_current_school_id),
):
    """Chat tarixini olish: course_id berilsa kurs chati, berilmasa global maktab chati."""
    from users.models import User

    query = (
        select(Message, User.full_name)
        .join(User, Message.sender_id == User.id)
        .where(Message.school_id == school_id)
    )
    if course_id:
        query = query.where(Message.course_id == course_id)
    else:
        query = query.where(Message.course_id.is_(None))
    res = await db.execute(query.order_by(Message.created_at.desc()).limit(50))
    rows = res.all()
    # Teskari tartibda qaytaramizki xronologik to'g'ri bo'lsin
    return [
        {"id": m.id, "content": m.content, "sender_id": m.sender_id, "sender": sender_name, "created_at": m.created_at}
        for m, sender_name in rows[::-1]
    ]
