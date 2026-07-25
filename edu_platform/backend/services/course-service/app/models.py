"""
course-service modellari.
Kurs strukturasi: Course -> Module -> Lesson -> (Quiz | Homework).
"""
from __future__ import annotations

import uuid

from sqlalchemy import String, Text, Integer, Numeric, Boolean, ForeignKey, JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.core.mixins import UUIDMixin, TimestampMixin
from libs.shared_schemas.enums import EnrollmentStatus


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Course(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "courses"

    school_id: Mapped[uuid.UUID] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    modules: Mapped[list["Module"]] = relationship(
        back_populates="course", cascade="all, delete-orphan", order_by="Module.order"
    )


class Module(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "modules"

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    order: Mapped[int] = mapped_column(Integer, default=0)

    course: Mapped["Course"] = relationship(back_populates="modules")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order"
    )


class Lesson(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "lessons"

    module_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("modules.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    kinescope_video_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_free_preview: Mapped[bool] = mapped_column(Boolean, default=False)

    module: Mapped["Module"] = relationship(back_populates="lessons")
    quiz: Mapped["Quiz | None"] = relationship(
        back_populates="lesson", uselist=False, cascade="all, delete-orphan"
    )
    homeworks: Mapped[list["Homework"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )


class Quiz(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "quizzes"

    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id"), unique=True)
    questions: Mapped[list] = mapped_column(JSON)
    passing_score: Mapped[int] = mapped_column(Integer, default=70)

    lesson: Mapped["Lesson"] = relationship(back_populates="quiz")


class Homework(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "homeworks"

    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    # "test", "matching", "fill_blank", "detailed_answer", "file_upload"
    homework_type: Mapped[str] = mapped_column(String(50), default="detailed_answer")
    instructions: Mapped[str] = mapped_column(Text)
    content_schema: Mapped[dict] = mapped_column(JSON, default=dict)  # Savollar, to'g'ri javoblar kaliti
    max_score: Mapped[int] = mapped_column(Integer, default=100)
    auto_check: Mapped[bool] = mapped_column(Boolean, default=False)

    lesson: Mapped["Lesson"] = relationship(back_populates="homeworks")
    submissions: Mapped[list["HomeworkSubmission"]] = relationship(
        back_populates="homework", cascade="all, delete-orphan"
    )


class HomeworkSubmission(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "homework_submissions"

    homework_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("homeworks.id"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    student_answer: Mapped[dict] = mapped_column(JSON)  # O'quvchi javobi yoki fayl URL
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, rejected
    reviewer_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)

    homework: Mapped["Homework"] = relationship(back_populates="submissions")


class Enrollment(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "enrollments"

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    status: Mapped[EnrollmentStatus] = mapped_column(default=EnrollmentStatus.active)
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)
