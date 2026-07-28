import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class TelegramBotSettings(Base):
    """Maktabning Telegram Bot integratsiyasi"""
    __tablename__ = "telegram_bot_settings"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), unique=True)
    
    bot_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    private_channel_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    invite_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
