import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Video(Base):
    __tablename__ = "videos"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    kinescope_id: Mapped[str] = mapped_column(String(100))
