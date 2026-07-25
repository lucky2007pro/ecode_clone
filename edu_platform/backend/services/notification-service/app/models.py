"""
notification-service modellari.
Boshqa servislar RabbitMQ orqali "notify.send" eventini yuboradi,
bu servis shablonni topib, kanal (email/sms/push) orqali jo'natadi
va natijani log qiladi.
"""
from __future__ import annotations

import uuid

from sqlalchemy import String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.mixins import UUIDMixin, TimestampMixin


class Base(AsyncAttrs, DeclarativeBase):
    pass


class NotificationTemplate(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "notification_templates"

    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)  # "welcome_email"
    channel: Mapped[str] = mapped_column(String(20))  # "email" | "sms" | "push"
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text)


class NotificationLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "notification_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)  # auth-service.User.id
    channel: Mapped[str] = mapped_column(String(20))
    template_code: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending|sent|failed
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
