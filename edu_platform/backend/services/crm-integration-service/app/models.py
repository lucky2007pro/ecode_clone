"""
crm-integration-service modellari.
Kommo bilan bog'liq holat shu yerda saqlanadi: lead/deal ID mosligi va
har bir sinxronizatsiya urinishining logi (nosozlikni tekshirish uchun
juda muhim, chunki Kommo API vaqti-vaqti bilan yiqiladi yoki
rate-limit qiladi).
"""
from __future__ import annotations

import uuid

from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.core.mixins import UUIDMixin, TimestampMixin
from libs.shared_schemas.enums import CrmSyncStatus


class Base(AsyncAttrs, DeclarativeBase):
    pass


class CrmLead(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "crm_leads"

    user_id: Mapped[uuid.UUID] = mapped_column(index=True, unique=True)  # auth-service.User.id
    kommo_lead_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    kommo_contact_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pipeline_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sync_status: Mapped[CrmSyncStatus] = mapped_column(default=CrmSyncStatus.pending)

    sync_logs: Mapped[list["CrmSyncLog"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan"
    )


class CrmSyncLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "crm_sync_logs"

    lead_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("crm_leads.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(100))  # "lead.created", "deal.status_changed"
    direction: Mapped[str] = mapped_column(String(20))  # "outbound" yoki "inbound"
    payload: Mapped[dict] = mapped_column(JSON)
    status: Mapped[CrmSyncStatus] = mapped_column(default=CrmSyncStatus.pending)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    lead: Mapped["CrmLead"] = relationship(back_populates="sync_logs")
