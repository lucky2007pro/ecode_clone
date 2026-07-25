"""
course-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from libs.shared_schemas.enums import EnrollmentStatus


# --- QUIZ SCHEMAS ---
class QuizBase(BaseModel):
    questions: list[dict]
    passing_score: int = 70


class QuizCreate(QuizBase):
    pass


class QuizResponse(QuizBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lesson_id: uuid.UUID
    created_at: datetime


# --- HOMEWORK SCHEMAS ---
class HomeworkBase(BaseModel):
    title: str
    homework_type: str = "detailed_answer"
    instructions: str
    content_schema: dict = {}
    max_score: int = 100
    auto_check: bool = False


class HomeworkCreate(HomeworkBase):
    lesson_id: uuid.UUID


class HomeworkResponse(HomeworkBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lesson_id: uuid.UUID
    created_at: datetime


class SubmissionCreate(BaseModel):
    homework_id: uuid.UUID
    user_id: uuid.UUID
    student_answer: dict


class SubmissionReview(BaseModel):
    score: int
    status: str  # "approved" | "rejected"
    reviewer_feedback: str | None = None
    reviewer_id: uuid.UUID


class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    homework_id: uuid.UUID
    user_id: uuid.UUID
    student_answer: dict
    score: int | None
    status: str
    reviewer_feedback: str | None
    created_at: datetime


# --- LESSON SCHEMAS ---
class LessonBase(BaseModel):
    title: str
    content: str | None = None
    order: int = 0
    is_free_preview: bool = False


class LessonCreate(LessonBase):
    module_id: uuid.UUID
    kinescope_video_id: str | None = None


class LessonUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    kinescope_video_id: str | None = None
    order: int | None = None
    is_free_preview: bool | None = None


class LessonResponse(LessonBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    module_id: uuid.UUID
    kinescope_video_id: str | None = None
    quiz: QuizResponse | None = None
    homeworks: list[HomeworkResponse] = []
    created_at: datetime


# --- MODULE SCHEMAS ---
class ModuleBase(BaseModel):
    title: str
    order: int = 0


class ModuleCreate(ModuleBase):
    course_id: uuid.UUID


class ModuleUpdate(BaseModel):
    title: str | None = None
    order: int | None = None


class ModuleResponse(ModuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    course_id: uuid.UUID
    lessons: list[LessonResponse] = []
    created_at: datetime


# --- COURSE SCHEMAS ---
class CourseBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    cover_url: str | None = None
    price: float = 0.0
    is_published: bool = False


class CourseCreate(CourseBase):
    school_id: uuid.UUID


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cover_url: str | None = None
    price: float | None = None
    is_published: bool | None = None


class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    school_id: uuid.UUID
    modules: list[ModuleResponse] = []
    created_at: datetime


# --- ENROLLMENT SCHEMAS ---
class EnrollmentCreate(BaseModel):
    course_id: uuid.UUID
    user_id: uuid.UUID


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    course_id: uuid.UUID
    user_id: uuid.UUID
    status: EnrollmentStatus
    progress_percent: int
    created_at: datetime
