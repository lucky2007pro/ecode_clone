import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from enrollments.models import EnrollmentStatus


class EnrollmentCreate(BaseModel):
    user_id: uuid.UUID
    course_id: uuid.UUID


class PurchaseRequest(BaseModel):
    course_id: uuid.UUID


class EnrollmentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    status: EnrollmentStatus
    progress: float
    full_name: Optional[str] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
