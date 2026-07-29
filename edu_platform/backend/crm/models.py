import uuid

from sqlalchemy import String, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column

from db import Base

class KommoSettings(Base):

    """
    Maktabning Kommo CRM integratsiya sozlamalari va OAuth kalitlari
    """

    __tablename__ = "kommo_settings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), unique=True)

    subdomain: Mapped[str] = mapped_column(String(100), nullable=True)

    client_id: Mapped[str] = mapped_column(String(255), nullable=True)

    client_secret: Mapped[str] = mapped_column(String(255), nullable=True)

    access_token: Mapped[str] = mapped_column(String(1000), nullable=True)

    refresh_token: Mapped[str] = mapped_column(String(1000), nullable=True)

class CrmLead(Base):

    __tablename__ = "crm_leads"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=True)

    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    kommo_id: Mapped[int] = mapped_column()

    status: Mapped[str] = mapped_column(String(50), default="created")

