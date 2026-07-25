import uuid
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
import enum

class UserRole(str, enum.Enum):
    school_owner = "school_owner"
    expert_teacher = "expert_teacher"
    producer = "producer"
    corporate_hr = "corporate_hr"
    student = "student"
    other = "other"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(default=UserRole.school_owner)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
