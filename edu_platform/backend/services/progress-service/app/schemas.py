"""
progress-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LessonProgressUpdate(BaseModel):
    course_id: uuid.UUID
    lesson_id: uuid.UUID
    is_completed: bool = True


class LessonProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    lesson_id: uuid.UUID
    is_completed: bool
    completed_at: datetime | None
    created_at: datetime


class CertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    certificate_number: str
    file_url: str
    created_at: datetime
