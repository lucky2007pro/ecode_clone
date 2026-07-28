import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from notifications.models import Notification
from users.models import User
from schools.models import UserSchool, MembershipStatus
from permissions.enums import Role


async def create_notification(db: AsyncSession, user_id: uuid.UUID, school_id, title: str, body: str | None = None) -> Notification:
    notification = Notification(user_id=user_id, school_id=school_id, title=title, body=body)
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def get_school_admin_ids(db: AsyncSession, school_id) -> list[uuid.UUID]:
    """Maktabning tasdiqlangan adminlari ID'lari (bildirishnoma yuborish uchun)."""
    res = await db.execute(
        select(User.id)
        .join(UserSchool, UserSchool.user_id == User.id)
        .where(UserSchool.school_id == school_id)
        .where(UserSchool.status == MembershipStatus.APPROVED)
        .where(User.role == Role.ADMIN)
    )
    return list(res.scalars().all())


async def get_school_teacher_ids(db: AsyncSession, school_id) -> list[uuid.UUID]:
    """Maktabning tasdiqlangan o'qituvchilari ID'lari (bildirishnoma yuborish uchun)."""
    res = await db.execute(
        select(User.id)
        .join(UserSchool, UserSchool.user_id == User.id)
        .where(UserSchool.school_id == school_id)
        .where(UserSchool.status == MembershipStatus.APPROVED)
        .where(User.role == Role.TEACHER)
    )
    return list(res.scalars().all())


async def get_user_notifications(db: AsyncSession, user_id: uuid.UUID) -> list[Notification]:
    res = await db.execute(
        select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
    )
    return res.scalars().all()


async def count_unread(db: AsyncSession, user_id: uuid.UUID) -> int:
    res = await db.execute(
        select(func.count()).select_from(Notification).where(Notification.user_id == user_id).where(Notification.is_read == False)  # noqa: E712
    )
    return res.scalar_one()


async def mark_notification_read(db: AsyncSession, notification_id: uuid.UUID, user_id: uuid.UUID) -> Notification | None:
    res = await db.execute(
        select(Notification).where(Notification.id == notification_id).where(Notification.user_id == user_id)
    )
    notification = res.scalar_one_or_none()
    if notification and not notification.is_read:
        notification.is_read = True
        await db.commit()
        await db.refresh(notification)
    return notification


async def mark_all_notifications_read(db: AsyncSession, user_id: uuid.UUID) -> None:
    await db.execute(
        update(Notification).where(Notification.user_id == user_id).where(Notification.is_read == False).values(is_read=True)  # noqa: E712
    )
    await db.commit()
