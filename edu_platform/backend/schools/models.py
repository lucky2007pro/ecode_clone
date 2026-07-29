import uuid

import enum

from sqlalchemy import String, Boolean, JSON, Text, ForeignKey, Enum as SQLEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class MembershipStatus(str, enum.Enum):

    PENDING = "pending"

    APPROVED = "approved"

    REJECTED = "rejected"

class School(Base):

    __tablename__ = "schools"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255))

    subdomain: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    custom_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)

    primary_color: Mapped[str] = mapped_column(String(20), default="#6366f1")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

class UserSchool(Base):

    __tablename__ = "user_schools"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id"))

    status: Mapped[MembershipStatus] = mapped_column(SQLEnum(MembershipStatus), default=MembershipStatus.PENDING)

