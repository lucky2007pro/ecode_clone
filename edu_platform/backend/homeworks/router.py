import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from homeworks.schema import HomeworkSubmissionCreate, HomeworkSubmissionResponse, GradeRequest
from homeworks.crud import submit_homework, get_all_submissions, get_lesson_submissions, get_student_submissions, grade_submission
from permissions.dependencies import RequirePermissions, get_current_school_id
from permissions.enums import Permission
from notifications.crud import create_notification, get_school_teacher_ids
from lessons.models import Lesson
from courses.models import Course

router = APIRouter()


@router.post("/", response_model=HomeworkSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(sub_in: HomeworkSubmissionCreate, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):
    """O'quvchi tomonidan uy vazifasi yuborish."""
    submission = await submit_homework(db, sub_in, school_id)
    # Shu kursning o'qituvchisiga bildirishnoma yuborish (adminga emas)
    teacher_id = await db.scalar(select(Course.teacher_id).join(Lesson, Lesson.course_id == Course.id).where(Lesson.id == sub_in.lesson_id))
    if teacher_id:
        teacher_ids = [teacher_id]
    else:
        # Kursga o'qituvchi biriktirilmagan bo'lsa, maktab teacher'lariga yuboramiz
        teacher_ids = await get_school_teacher_ids(db, school_id)
    for teacher_id in teacher_ids:
        await create_notification(
            db, teacher_id, school_id,
            "Yangi uy vazifasi yuborildi",
            "Darsga yangi uy vazifasi yuborildi, tekshirib chiqing"
        )
    return submission


@router.get("/", response_model=List[HomeworkSubmissionResponse])
async def list_all_submissions(db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id), _=Depends(RequirePermissions([Permission.GRADE_HOMEWORKS]))):
    """Barcha uy vazifalarini ko'rish (Curator/Admin uchun)."""
    return await get_all_submissions(db, school_id)


@router.get("/student/{student_id}", response_model=List[HomeworkSubmissionResponse])
async def list_student_submissions(student_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id), _=Depends(RequirePermissions([Permission.GRADE_HOMEWORKS]))):
    """Muayyan o'quvchining uy vazifalarini ko'rish."""
    return await get_student_submissions(db, student_id, school_id)


@router.get("/lesson/{lesson_id}", response_model=List[HomeworkSubmissionResponse])
async def list_lesson_submissions(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id), _=Depends(RequirePermissions([Permission.GRADE_HOMEWORKS]))):
    """Muayyan darsning uy vazifalarini ko'rish."""
    return await get_lesson_submissions(db, lesson_id, school_id)


@router.post("/{sub_id}/grade", response_model=HomeworkSubmissionResponse)
async def grade_homework(sub_id: uuid.UUID, req: GradeRequest, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id), _=Depends(RequirePermissions([Permission.GRADE_HOMEWORKS]))):
    """Uy vazifasini baholash va fikr bildirish (Curator)."""
    submission = await grade_submission(db, sub_id, req, school_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Uy vazifasi topilmadi")
    # O'quvchiga baholanishi haqida bildirishnoma
    await create_notification(
        db, submission.student_id, school_id,
        "Uy vazifangiz baholandi",
        f"Baho: {submission.grade}. Fikr: {submission.feedback}"
    )
    return submission
