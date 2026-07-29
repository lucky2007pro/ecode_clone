import uuid

from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

class QuizAnswerCreate(BaseModel):

    text: str

    is_correct: bool

class QuizAnswerResponse(BaseModel):

    id: uuid.UUID

    text: str

    is_correct: bool

    model_config = ConfigDict(from_attributes=True)

class QuizQuestionCreate(BaseModel):

    text: str

    order: int = 0

    answers: List[QuizAnswerCreate]

class QuizQuestionResponse(BaseModel):

    id: uuid.UUID

    text: str

    order: int

    answers: List[QuizAnswerResponse] = []

    model_config = ConfigDict(from_attributes=True)

class QuizCreate(BaseModel):

    lesson_id: uuid.UUID

    title: str

    passing_score: int = 50

class QuizResponse(BaseModel):

    id: uuid.UUID

    lesson_id: uuid.UUID

    title: str

    passing_score: int

    model_config = ConfigDict(from_attributes=True)

class QuizTakeAnswer(BaseModel):

    id: uuid.UUID

    text: str

    model_config = ConfigDict(from_attributes=True)

class QuizQuestionTake(BaseModel):

    id: uuid.UUID

    text: str

    order: int

    answers: List[QuizTakeAnswer] = []

    model_config = ConfigDict(from_attributes=True)

class QuizSubmitRequest(BaseModel):

    answers: dict[uuid.UUID, uuid.UUID]

class QuizSubmitResponse(BaseModel):

    score: int

    total: int

    percent: int

class QuizResultResponse(BaseModel):

    id: uuid.UUID

    quiz_id: uuid.UUID

    student_id: uuid.UUID

    score: int

    total: int

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

