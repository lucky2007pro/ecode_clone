import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class MarketingSettings(Base):
    """Maktabning marketing sozlamalari (Piksellar, UTM, Google Analytics)"""
    __tablename__ = "marketing_settings"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), unique=True)
    
    facebook_pixel_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    google_analytics_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    yandex_metrika_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
