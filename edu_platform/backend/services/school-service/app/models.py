"""
school-service modellari.
Multi-tenant maktablar: domeni, brending sozlamalari (White-Label), SSL va tarif rejasi.
"""
from __future__ import annotations

import uuid

from sqlalchemy import String, Integer, Numeric, ForeignKey, JSON, Boolean, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.core.mixins import UUIDMixin, TimestampMixin


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TariffPlan(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "tariff_plans"

    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    max_students: Mapped[int] = mapped_column(Integer)
    max_courses: Mapped[int] = mapped_column(Integer)
    max_storage_gb: Mapped[int] = mapped_column(Integer, default=10)


class School(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(String(255))
    subdomain: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    custom_domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    owner_id: Mapped[uuid.UUID] = mapped_column(index=True)

    # White-Label Brending va kastomizatsiya
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    primary_color: Mapped[str] = mapped_column(String(20), default="#6366f1")
    secondary_color: Mapped[str] = mapped_column(String(20), default="#a855f7")
    custom_css: Mapped[str | None] = mapped_column(Text, nullable=True)

    # SSL sertifikat holati (custom_domain uchun)
    ssl_active: Mapped[bool] = mapped_column(Boolean, default=False)

    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    tariff_plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tariff_plans.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tariff_plan: Mapped["TariffPlan"] = relationship()
