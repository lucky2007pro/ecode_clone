import uuid
from pydantic import BaseModel
from enrollments.models import EnrollmentStatus


class EnrollmentCreate(BaseModel):
    user_id: uuid.UUID
    course_id: uuid.UUID


class EnrollmentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    status: EnrollmentStatus
    progress: float

    class Config:
        from_attributes = True
