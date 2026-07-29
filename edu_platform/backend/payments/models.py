import uuid

from datetime import datetime, timezone

from sqlalchemy import String, Numeric, Float, ForeignKey, DateTime, Boolean, Enum as SQLAlchemyEnum

from sqlalchemy.orm import Mapped, mapped_column

from db import Base

import enum

class PlanType(enum.Enum):

    ONE_TIME = "one_time"

    INSTALLMENT = "installment"

    SUBSCRIPTION = "subscription"

class SubscriptionStatus(enum.Enum):

    ACTIVE = "active"

    PAST_DUE = "past_due"

    CANCELED = "canceled"

class Payment(Base):

    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    amount: Mapped[float] = mapped_column(Numeric(10, 2))

    provider: Mapped[str] = mapped_column(String(50))

class PaymentPlan(Base):

    """Kurslar uchun to'lov rejalari (Masalan: 3 oyga bo'lib to'lash)"""

    __tablename__ = "payment_plans"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), index=True)

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)

    name: Mapped[str] = mapped_column(String(255))

    plan_type: Mapped[PlanType] = mapped_column(SQLAlchemyEnum(PlanType))

    price: Mapped[float] = mapped_column(Float)

    months: Mapped[int] = mapped_column(default=1)

class Subscription(Base):

    """O'quvchining obunasi yoki muddatli to'lovi holati"""

    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), index=True)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("payment_plans.id", ondelete="CASCADE"))

    status: Mapped[SubscriptionStatus] = mapped_column(SQLAlchemyEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)

    next_payment_date: Mapped[datetime] = mapped_column(DateTime)

    auto_charge: Mapped[bool] = mapped_column(Boolean, default=True)

class TransactionType(enum.Enum):

    IN = "in"

    OUT = "out"

class Transaction(Base):

    """Barcha to'lov operatsiyalari tarixi"""

    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), index=True, nullable=True)

    amount: Mapped[float] = mapped_column(Numeric(10, 2))

    type: Mapped[TransactionType] = mapped_column(SQLAlchemyEnum(TransactionType))

    description: Mapped[str] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

class SchoolSubscription(Base):

    """Maktabning platforma uchun obunasi"""

    __tablename__ = "school_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), index=True)

    plan_name: Mapped[str] = mapped_column(String(100))

    status: Mapped[SubscriptionStatus] = mapped_column(SQLAlchemyEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)

    expires_at: Mapped[datetime] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

