import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from quizzes.models import Quiz, QuizQuestion, QuizAnswer, QuizResult

from quizzes.schema import QuizCreate, QuizQuestionCreate

async def get_quiz_by_lesson(db: AsyncSession, lesson_id: uuid.UUID, school_id):

    res = await db.execute(select(Quiz).where(Quiz.lesson_id == lesson_id).where(Quiz.school_id == school_id))

    return res.scalar_one_or_none()

async def get_quiz_by_id(db: AsyncSession, quiz_id: uuid.UUID, school_id):

    res = await db.execute(select(Quiz).where(Quiz.id == quiz_id).where(Quiz.school_id == school_id))

    return res.scalar_one_or_none()

async def create_quiz(db: AsyncSession, quiz_in: QuizCreate, school_id):

    quiz = Quiz(

        lesson_id=quiz_in.lesson_id, school_id=school_id,

        title=quiz_in.title,

        passing_score=quiz_in.passing_score

    )

    db.add(quiz)

    await db.commit()

    await db.refresh(quiz)

    return quiz

async def get_questions_by_quiz(db: AsyncSession, quiz_id: uuid.UUID):

    res = await db.execute(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.order))

    return res.scalars().all()

async def get_answers_by_question(db: AsyncSession, question_id: uuid.UUID):

    res = await db.execute(select(QuizAnswer).where(QuizAnswer.question_id == question_id))

    return res.scalars().all()

async def add_question_with_answers(db: AsyncSession, quiz_id: uuid.UUID, q_in: QuizQuestionCreate):

    question = QuizQuestion(quiz_id=quiz_id, text=q_in.text, order=q_in.order)

    db.add(question)

    await db.commit()

    await db.refresh(question)

    for ans_in in q_in.answers:

        ans = QuizAnswer(question_id=question.id, text=ans_in.text, is_correct=ans_in.is_correct)

        db.add(ans)

    await db.commit()

    return question

async def save_quiz_result(db: AsyncSession, quiz_id: uuid.UUID, student_id: uuid.UUID, school_id, score: int, total: int) -> QuizResult:

    result = QuizResult(quiz_id=quiz_id, student_id=student_id, school_id=school_id, score=score, total=total)

    db.add(result)

    await db.commit()

    await db.refresh(result)

    return result

async def get_quiz_results_by_student(db: AsyncSession, student_id: uuid.UUID, school_id) -> list[QuizResult]:

    res = await db.execute(

        select(QuizResult)

        .where(QuizResult.student_id == student_id)

        .where(QuizResult.school_id == school_id)

        .order_by(QuizResult.created_at.desc())

    )

    return res.scalars().all()

