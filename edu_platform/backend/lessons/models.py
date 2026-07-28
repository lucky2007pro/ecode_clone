import uuid
import enum
from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class LessonType(str, enum.Enum):
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"


class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    lesson_type: Mapped[LessonType] = mapped_column(
        SqlEnum(LessonType, values_callable=lambda x: [e.value for e in x]),
        default=LessonType.VIDEO
    )
    order: Mapped[int] = mapped_column(Integer, default=0)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
