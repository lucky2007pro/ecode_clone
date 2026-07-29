import uuid

from typing import Optional

from pydantic import BaseModel, ConfigDict

from homeworks.models import HomeworkStatus

class HomeworkSubmissionCreate(BaseModel):

    lesson_id: uuid.UUID

    student_id: uuid.UUID

    submission_text: str

class GradeRequest(BaseModel):

    grade: int

    status: HomeworkStatus

    feedback: str

class HomeworkSubmissionResponse(BaseModel):

    id: uuid.UUID

    lesson_id: uuid.UUID

    student_id: uuid.UUID

    submission_text: str

    status: HomeworkStatus

    grade: Optional[int] = None

    feedback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

