import uuid
from pydantic import BaseModel
from lessons.models import LessonType


class LessonCreate(BaseModel):
    course_id: uuid.UUID
    title: str
    content: str | None = None
    video_url: str | None = None
    lesson_type: LessonType = LessonType.VIDEO
    order: int = 0
    duration_minutes: int = 0


class LessonResponse(LessonCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True
