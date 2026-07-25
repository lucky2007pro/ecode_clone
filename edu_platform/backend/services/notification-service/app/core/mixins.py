"""
Umumiy SQLAlchemy mixinlar. Bu faylni har bir servis o'z
app/core/mixins.py sifatida nusxalaydi (yoki libs paketidan import qiladi).
Maqsad - har bir servisda id/created_at/updated_at ustunlarini
qayta-qayta yozmaslik.
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
