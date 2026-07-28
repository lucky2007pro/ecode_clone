import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from quizzes.schema import QuizCreate, QuizResponse, QuizQuestionCreate, QuizQuestionResponse, QuizAnswerResponse
from quizzes.crud import get_quiz_by_lesson, create_quiz, get_questions_by_quiz, get_answers_by_question, add_question_with_answers

router = APIRouter()


@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_new_quiz(quiz_in: QuizCreate, db: AsyncSession = Depends(get_db)):
    """Dars uchun yangi test (Quiz) yaratish."""
    existing = await get_quiz_by_lesson(db, quiz_in.lesson_id)
    if existing:
        raise HTTPException(status_code=400, detail="Ushbu dars uchun test allaqachon mavjud")
    return await create_quiz(db, quiz_in)


@router.get("/lesson/{lesson_id}", response_model=QuizResponse)
async def get_lesson_quiz(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Darsga tegishli testni olish."""
    quiz = await get_quiz_by_lesson(db, lesson_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Test topilmadi")
    return quiz


@router.post("/{quiz_id}/questions", status_code=status.HTTP_201_CREATED)
async def add_quiz_question(quiz_id: uuid.UUID, q_in: QuizQuestionCreate, db: AsyncSession = Depends(get_db)):
    """Testga yangi savol va uning javoblarini qo'shish."""
    question = await add_question_with_answers(db, quiz_id, q_in)
    return {"status": "success", "question_id": question.id}


@router.get("/{quiz_id}/questions/full", response_model=list[QuizQuestionResponse])
async def get_full_quiz_questions(quiz_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Testning barcha savollari va javob variantlarini olish."""
    questions = await get_questions_by_quiz(db, quiz_id)
    result = []
    for q in questions:
        answers = await get_answers_by_question(db, q.id)
        ans_list = [QuizAnswerResponse.model_validate(a) for a in answers]
        q_resp = QuizQuestionResponse(id=q.id, text=q.text, order=q.order, answers=ans_list)
        result.append(q_resp)
    return result
