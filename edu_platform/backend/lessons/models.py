import uuid

import enum

from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SqlEnum

from sqlalchemy.orm import Mapped, mapped_column

from db import Base

class LessonType(str, enum.Enum):

    VIDEO = "video"

    TEXT = "text"

    QUIZ = "quiz"

class CourseModule(Base):

    __tablename__ = "modules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), index=True)

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), index=True)

    title: Mapped[str] = mapped_column(String(255))

    order: Mapped[int] = mapped_column(Integer, default=0)

class Lesson(Base):

    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), index=True)

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), index=True)

    module_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("modules.id"), nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(255))

    content: Mapped[str | None] = mapped_column(Text, nullable=True)

    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    lesson_type: Mapped[LessonType] = mapped_column(

        SqlEnum(LessonType, values_callable=lambda x: [e.value for e in x]),

        default=LessonType.VIDEO

    )

    order: Mapped[int] = mapped_column(Integer, default=0)

    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)

