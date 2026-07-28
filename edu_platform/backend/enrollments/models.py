import uuid
import enum
from sqlalchemy import ForeignKey, Enum as SqlEnum, Float
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"


class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), index=True)
    status: Mapped[EnrollmentStatus] = mapped_column(
        SqlEnum(EnrollmentStatus, values_callable=lambda x: [e.value for e in x]),
        default=EnrollmentStatus.ACTIVE
    )
    progress: Mapped[float] = mapped_column(Float, default=0.0)
