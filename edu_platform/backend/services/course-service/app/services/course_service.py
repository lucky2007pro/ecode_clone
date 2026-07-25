"""
course-service biznes mantiqiy servisi (Course, Module, Lesson, Quiz, Homework, Enrollment).
"""
import uuid
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models import Course, Module, Lesson, Quiz, Homework, HomeworkSubmission, Enrollment
from app.schemas import (
    CourseCreate,
    CourseUpdate,
    ModuleCreate,
    ModuleUpdate,
    LessonCreate,
    LessonUpdate,
    QuizCreate,
    HomeworkCreate,
    SubmissionCreate,
    SubmissionReview,
    EnrollmentCreate,
)


# --- COURSE SERVICES ---
async def create_course(db: AsyncSession, course_in: CourseCreate) -> Course:
    stmt = select(Course).where(Course.slug == course_in.slug)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday slug bilan kurs allaqachon mavjud",
        )

    course = Course(**course_in.model_dump())
    db.add(course)
    await db.flush()
    return course


async def get_courses_by_school(
    db: AsyncSession, school_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[Course]:
    stmt = (
        select(Course)
        .where(Course.school_id == school_id)
        .options(selectinload(Course.modules).selectinload(Module.lessons).selectinload(Lesson.homeworks))
        .offset(skip)
        .limit(limit)
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def get_course_by_id(db: AsyncSession, course_id: uuid.UUID) -> Course:
    stmt = (
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.modules).selectinload(Module.lessons).selectinload(Lesson.homeworks))
    )
    res = await db.execute(stmt)
    course = res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi")
    return course


async def update_course(
    db: AsyncSession, course_id: uuid.UUID, course_update: CourseUpdate
) -> Course:
    course = await get_course_by_id(db, course_id)
    update_data = course_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(course, field, value)

    await db.flush()
    return course


# --- MODULE SERVICES ---
async def create_module(db: AsyncSession, module_in: ModuleCreate) -> Module:
    module = Module(**module_in.model_dump())
    db.add(module)
    await db.flush()
    return module


async def get_modules_by_course(db: AsyncSession, course_id: uuid.UUID) -> list[Module]:
    stmt = (
        select(Module)
        .where(Module.course_id == course_id)
        .options(selectinload(Module.lessons).selectinload(Lesson.homeworks))
        .order_by(Module.order)
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())


# --- LESSON SERVICES ---
async def create_lesson(db: AsyncSession, lesson_in: LessonCreate) -> Lesson:
    lesson = Lesson(**lesson_in.model_dump())
    db.add(lesson)
    await db.flush()
    return lesson


async def get_lesson_by_id(db: AsyncSession, lesson_id: uuid.UUID) -> Lesson:
    stmt = (
        select(Lesson)
        .where(Lesson.id == lesson_id)
        .options(selectinload(Lesson.quiz), selectinload(Lesson.homeworks))
    )
    res = await db.execute(stmt)
    lesson = res.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Dars topilmadi")
    return lesson


async def update_lesson(
    db: AsyncSession, lesson_id: uuid.UUID, lesson_update: LessonUpdate
) -> Lesson:
    lesson = await get_lesson_by_id(db, lesson_id)
    update_data = lesson_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(lesson, field, value)

    await db.flush()
    return lesson


# --- HOMEWORK & SUBMISSION SERVICES ---
async def create_homework(db: AsyncSession, hw_in: HomeworkCreate) -> Homework:
    hw = Homework(**hw_in.model_dump())
    db.add(hw)
    await db.flush()
    return hw


async def submit_homework(db: AsyncSession, sub_in: SubmissionCreate) -> HomeworkSubmission:
    hw = await db.get(Homework, sub_in.homework_id)
    if not hw:
        raise HTTPException(status_code=404, detail="Uy vazifasi topilmadi")

    # Avto-tekshirish mantiqi (agar auto_check=True bo'lsa)
    score = None
    status_str = "pending"

    if hw.auto_check and hw.content_schema and "correct_answers" in hw.content_schema:
        correct = hw.content_schema.get("correct_answers", {})
        student_ans = sub_in.student_answer.get("answers", {})

        total = len(correct)
        match_count = 0
        for k, v in correct.items():
            if str(student_ans.get(k)) == str(v):
                match_count += 1

        if total > 0:
            calculated = int((match_count / total) * hw.max_score)
            score = calculated
            status_str = "approved" if calculated >= (hw.max_score * 0.6) else "rejected"

    submission = HomeworkSubmission(
        homework_id=sub_in.homework_id,
        user_id=sub_in.user_id,
        student_answer=sub_in.student_answer,
        score=score,
        status=status_str,
    )
    db.add(submission)
    await db.flush()
    return submission


async def review_homework_submission(
    db: AsyncSession, submission_id: uuid.UUID, review_in: SubmissionReview
) -> HomeworkSubmission:
    sub = await db.get(HomeworkSubmission, submission_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Javob topilmadi")

    sub.score = review_in.score
    sub.status = review_in.status
    sub.reviewer_feedback = review_in.reviewer_feedback
    sub.reviewer_id = review_in.reviewer_id

    await db.flush()
    return sub


# --- ENROLLMENT SERVICES ---
async def enroll_user(db: AsyncSession, enroll_in: EnrollmentCreate) -> Enrollment:
    stmt = select(Enrollment).where(
        Enrollment.course_id == enroll_in.course_id,
        Enrollment.user_id == enroll_in.user_id,
    )
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foydalanuvchi allaqachon ushbu kursga a'zo bo'lgan",
        )

    enrollment = Enrollment(
        course_id=enroll_in.course_id,
        user_id=enroll_in.user_id,
    )
    db.add(enrollment)
    await db.flush()
    return enrollment


async def get_user_enrollments(db: AsyncSession, user_id: uuid.UUID) -> list[Enrollment]:
    stmt = select(Enrollment).where(Enrollment.user_id == user_id)
    res = await db.execute(stmt)
    return list(res.scalars().all())
