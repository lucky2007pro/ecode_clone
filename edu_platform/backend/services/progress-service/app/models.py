"""
progress-service modellari.
O'quvchining har bir darsdagi holati va yakuniy sertifikatlar shu yerda
saqlanadi. course-service.Enrollment.progress_percent bu servisdan
kelgan hisob-kitob asosida event orqali yangilanadi.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.mixins import UUIDMixin, TimestampMixin


class Base(AsyncAttrs, DeclarativeBase):
    pass


class LessonProgress(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "lesson_progress"

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)  # auth-service.User.id
    course_id: Mapped[uuid.UUID] = mapped_column(index=True)  # course-service.Course.id
    lesson_id: Mapped[uuid.UUID] = mapped_column(index=True)  # course-service.Lesson.id
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Certificate(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "certificates"

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(index=True)
    certificate_number: Mapped[str] = mapped_column(String(50), unique=True)
    file_url: Mapped[str] = mapped_column(String(500))
