import uuid

from typing import Optional

from pydantic import BaseModel, ConfigDict

from lessons.models import LessonType

class CourseModuleCreate(BaseModel):

    course_id: uuid.UUID

    title: str

    order: int = 0

class CourseModuleResponse(CourseModuleCreate):

    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class LessonCreate(BaseModel):

    course_id: uuid.UUID

    module_id: Optional[uuid.UUID] = None

    title: str

    content: str | None = None

    video_url: str | None = None

    lesson_type: LessonType = LessonType.VIDEO

    order: int = 0

    duration_minutes: int = 0

class LessonResponse(LessonCreate):

    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

