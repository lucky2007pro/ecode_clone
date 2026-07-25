import uuid
from sqlalchemy import String, Boolean, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class School(Base):
    __tablename__ = "schools"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    subdomain: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    custom_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    primary_color: Mapped[str] = mapped_column(String(20), default="#6366f1")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
