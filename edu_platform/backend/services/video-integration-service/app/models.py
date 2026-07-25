"""
video-integration-service modellari.
Kinescope bilan bog'liq BARCHA holat shu yerda saqlanadi: yuklash holati,
kodlash statusi, tomosha statistikasi. course-service faqat tayyor
kinescope_video_id'ni oladi (webhook orqali), qolgan hammasi shu servisda.
"""
from __future__ import annotations

import uuid

from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.core.mixins import UUIDMixin, TimestampMixin
from libs.shared_schemas.enums import VideoStatus


class Base(AsyncAttrs, DeclarativeBase):
    pass


class VideoAsset(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "video_assets"

    lesson_id: Mapped[uuid.UUID] = mapped_column(index=True)  # course-service.Lesson.id
    kinescope_video_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    upload_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[VideoStatus] = mapped_column(default=VideoStatus.uploading)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    watch_logs: Mapped[list["VideoWatchLog"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )


class VideoWatchLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "video_watch_logs"

    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("video_assets.id"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(index=True)  # auth-service.User.id
    watched_seconds: Mapped[int] = mapped_column(Integer, default=0)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    video: Mapped["VideoAsset"] = relationship(back_populates="watch_logs")
