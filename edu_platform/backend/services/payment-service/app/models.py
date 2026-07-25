"""
payment-service modellari.
To'lovlar, bo'lib-bo'lib to'lash (Installments) va obuna holatlari.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, Numeric, DateTime, Boolean, Integer, ForeignKey, JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.core.mixins import UUIDMixin, TimestampMixin
from libs.shared_schemas.enums import PaymentStatus


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Payment(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "payments"

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    course_id: Mapped[uuid.UUID | None] = mapped_column(index=True, nullable=True)
    school_id: Mapped[uuid.UUID] = mapped_column(index=True)

    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(10), default="UZS")
    provider: Mapped[str] = mapped_column(String(50))  # "payme", "click", "uzum"
    provider_transaction_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.pending)


class InstallmentPlan(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "installment_plans"

    course_id: Mapped[uuid.UUID] = mapped_column(index=True)
    total_months: Mapped[int] = mapped_column(Integer, default=3)  # 3, 6, 12 oy
    monthly_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class UserInstallment(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "user_installments"

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    installment_plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("installment_plans.id"), index=True)
    paid_months: Mapped[int] = mapped_column(Integer, default=0)
    card_token: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Payme Card Token for Auto-debit
    next_payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, completed, overdue


class Subscription(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "subscriptions"

    school_id: Mapped[uuid.UUID] = mapped_column(index=True)
    tariff_plan_id: Mapped[uuid.UUID] = mapped_column(index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
