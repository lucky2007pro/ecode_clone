import uuid
from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    slug: str
    description: str | None = None
    price: float = 0.0

class CourseResponse(CourseCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True
