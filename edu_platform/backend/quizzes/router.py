import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

from quizzes.schema import (

    QuizCreate, QuizResponse, QuizQuestionCreate, QuizQuestionResponse, QuizAnswerResponse,

    QuizQuestionTake, QuizTakeAnswer, QuizSubmitRequest, QuizSubmitResponse, QuizResultResponse,

)

from quizzes.crud import (

    get_quiz_by_lesson, get_quiz_by_id, create_quiz, get_questions_by_quiz,

    get_answers_by_question, add_question_with_answers, save_quiz_result, get_quiz_results_by_student,

)

from permissions.dependencies import get_current_school_id, get_current_user

router = APIRouter()

@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)

async def create_new_quiz(quiz_in: QuizCreate, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Dars uchun yangi test (Quiz) yaratish."""

    existing = await get_quiz_by_lesson(db, quiz_in.lesson_id, school_id)

    if existing:

        raise HTTPException(status_code=400, detail="Ushbu dars uchun test allaqachon mavjud")

    return await create_quiz(db, quiz_in, school_id)

@router.get("/lesson/{lesson_id}", response_model=QuizResponse)

async def get_lesson_quiz(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Darsga tegishli testni olish."""

    quiz = await get_quiz_by_lesson(db, lesson_id, school_id)

    if not quiz:

        raise HTTPException(status_code=404, detail="Test topilmadi")

    return quiz

@router.post("/{quiz_id}/questions", status_code=status.HTTP_201_CREATED)

async def add_quiz_question(quiz_id: uuid.UUID, q_in: QuizQuestionCreate, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Testga yangi savol va uning javoblarini qo'shish."""

    quiz = await get_quiz_by_id(db, quiz_id, school_id)

    if not quiz:

        raise HTTPException(status_code=404, detail="Test topilmadi")

    question = await add_question_with_answers(db, quiz_id, q_in)

    return {"status": "success", "question_id": question.id}

@router.get("/{quiz_id}/questions/full", response_model=list[QuizQuestionResponse])

async def get_full_quiz_questions(quiz_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Testning barcha savollari va javob variantlarini olish."""

    questions = await get_questions_by_quiz(db, quiz_id)

    result = []

    for q in questions:

        answers = await get_answers_by_question(db, q.id)

        ans_list = [QuizAnswerResponse.model_validate(a) for a in answers]

        q_resp = QuizQuestionResponse(id=q.id, text=q.text, order=q.order, answers=ans_list)

        result.append(q_resp)

    return result

@router.get("/results/my", response_model=list[QuizResultResponse])

async def get_my_quiz_results(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user), school_id=Depends(get_current_school_id)):

    """Joriy foydalanuvchining test natijalari."""

    return await get_quiz_results_by_student(db, current_user.id, school_id)

@router.get("/{quiz_id}/take", response_model=list[QuizQuestionTake])

async def take_quiz(quiz_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """O'quvchi uchun savollar — to'g'ri javob belgisi (is_correct) yashiringan."""

    quiz = await get_quiz_by_id(db, quiz_id, school_id)

    if not quiz:

        raise HTTPException(status_code=404, detail="Test topilmadi")

    questions = await get_questions_by_quiz(db, quiz_id)

    result = []

    for q in questions:

        answers = await get_answers_by_question(db, q.id)

        ans_list = [QuizTakeAnswer.model_validate(a) for a in answers]

        result.append(QuizQuestionTake(id=q.id, text=q.text, order=q.order, answers=ans_list))

    return result

@router.post("/{quiz_id}/submit", response_model=QuizSubmitResponse)

async def submit_quiz(quiz_id: uuid.UUID, submit_in: QuizSubmitRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user), school_id=Depends(get_current_school_id)):

    """Javoblarni serverda baholab, natijani saqlaydi."""

    quiz = await get_quiz_by_id(db, quiz_id, school_id)

    if not quiz:

        raise HTTPException(status_code=404, detail="Test topilmadi")

    questions = await get_questions_by_quiz(db, quiz_id)

    total = len(questions)

    score = 0

    for q in questions:

        answers = await get_answers_by_question(db, q.id)

        correct_ids = {a.id for a in answers if a.is_correct}

        if submit_in.answers.get(q.id) in correct_ids:

            score += 1

    percent = round(score * 100 / total) if total else 0

    await save_quiz_result(db, quiz_id, current_user.id, school_id, score, total)

    return QuizSubmitResponse(score=score, total=total, percent=percent)

