import uuid
from typing import List, Optional
from pydantic import BaseModel


class QuizAnswerCreate(BaseModel):
    text: str
    is_correct: bool


class QuizAnswerResponse(BaseModel):
    id: uuid.UUID
    text: str
    # is_correct not exposed to students, but admin needs it. For MVP, we expose it or use a separate endpoint
    is_correct: bool 

    class Config:
        from_attributes = True


class QuizQuestionCreate(BaseModel):
    text: str
    order: int = 0
    answers: List[QuizAnswerCreate]


class QuizQuestionResponse(BaseModel):
    id: uuid.UUID
    text: str
    order: int
    answers: List[QuizAnswerResponse] = []

    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    lesson_id: uuid.UUID
    title: str
    passing_score: int = 50


class QuizResponse(BaseModel):
    id: uuid.UUID
    lesson_id: uuid.UUID
    title: str
    passing_score: int

    class Config:
        from_attributes = True
