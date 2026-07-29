import uuid

import enum

from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SqlEnum

from sqlalchemy.orm import Mapped, mapped_column

from db import Base

class HomeworkStatus(str, enum.Enum):

    PENDING = "Sent for Review"

    APPROVED = "Approved"

    REJECTED = "Rejected"

class HomeworkSubmission(Base):

    __tablename__ = "homework_submissions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), index=True)

    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id"), index=True)

    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)

    submission_text: Mapped[str] = mapped_column(Text)

    status: Mapped[HomeworkStatus] = mapped_column(

        SqlEnum(HomeworkStatus, values_callable=lambda x: [e.value for e in x]),

        default=HomeworkStatus.PENDING

    )

    grade: Mapped[int | None] = mapped_column(Integer, nullable=True)

    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)

