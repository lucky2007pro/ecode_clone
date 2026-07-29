import uuid

from pydantic import BaseModel, ConfigDict

class CourseCreate(BaseModel):

    title: str

    slug: str

    description: str | None = None

    price: float = 0.0

class CourseResponse(CourseCreate):

    id: uuid.UUID

    teacher_id: uuid.UUID | None = None

    lessons_count: int = 0

    model_config = ConfigDict(from_attributes=True)

