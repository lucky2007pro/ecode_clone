import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from homeworks.schema import HomeworkSubmissionCreate, HomeworkSubmissionResponse, GradeRequest
from homeworks.crud import submit_homework, get_all_submissions, get_lesson_submissions, get_student_submissions, grade_submission

router = APIRouter()


@router.post("/", response_model=HomeworkSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(sub_in: HomeworkSubmissionCreate, db: AsyncSession = Depends(get_db)):
    """O'quvchi tomonidan uy vazifasi yuborish."""
    return await submit_homework(db, sub_in)


@router.get("/", response_model=List[HomeworkSubmissionResponse])
async def list_all_submissions(db: AsyncSession = Depends(get_db)):
    """Barcha uy vazifalarini ko'rish (Curator/Admin uchun)."""
    return await get_all_submissions(db)


@router.get("/student/{student_id}", response_model=List[HomeworkSubmissionResponse])
async def list_student_submissions(student_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Muayyan o'quvchining uy vazifalarini ko'rish."""
    return await get_student_submissions(db, student_id)


@router.get("/lesson/{lesson_id}", response_model=List[HomeworkSubmissionResponse])
async def list_lesson_submissions(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Muayyan darsning uy vazifalarini ko'rish."""
    return await get_lesson_submissions(db, lesson_id)


@router.post("/{sub_id}/grade", response_model=HomeworkSubmissionResponse)
async def grade_homework(sub_id: uuid.UUID, req: GradeRequest, db: AsyncSession = Depends(get_db)):
    """Uy vazifasini baholash va fikr bildirish (Curator)."""
    submission = await grade_submission(db, sub_id, req)
    if not submission:
        raise HTTPException(status_code=404, detail="Uy vazifasi topilmadi")
    return submission
