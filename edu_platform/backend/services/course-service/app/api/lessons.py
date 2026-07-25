"""
Lessons, Quiz & Homework API Router.
"""
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    QuizCreate,
    QuizResponse,
    HomeworkCreate,
    HomeworkResponse,
    SubmissionCreate,
    SubmissionResponse,
    SubmissionReview,
)
from app.services.course_service import (
    create_lesson,
    get_lesson_by_id,
    update_lesson,
    create_or_update_quiz,
    create_homework,
    submit_homework,
    review_homework_submission,
)

router = APIRouter()


@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_new_lesson(lesson_in: LessonCreate, db: AsyncSession = Depends(get_db)):
    """Modul ichida dars yaratish."""
    return await create_lesson(db, lesson_in)


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Darsni to'liq quiz va uy vazifalari bilan olish."""
    return await get_lesson_by_id(db, lesson_id)


@router.patch("/{lesson_id}", response_model=LessonResponse)
async def patch_lesson(
    lesson_id: uuid.UUID,
    lesson_update: LessonUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Darsni tahrirlash (masalan video ID biriktirish)."""
    return await update_lesson(db, lesson_id, lesson_update)


# --- HOMEWORK ENDPOINTS ---
@router.post("/homework", response_model=HomeworkResponse, status_code=status.HTTP_201_CREATED)
async def add_homework(hw_in: HomeworkCreate, db: AsyncSession = Depends(get_db)):
    """Darsga yangi uy vazifasi qo'shish (7 xil turdagi)."""
    return await create_homework(db, hw_in)


@router.post("/homework/submit", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_student_homework(sub_in: SubmissionCreate, db: AsyncSession = Depends(get_db)):
    """O'quvchi uy vazifasi javobini topshirishi (Avto-tekshiruv yoki Kuratorga ketadi)."""
    return await submit_homework(db, sub_in)


@router.patch("/homework/submission/{submission_id}/review", response_model=SubmissionResponse)
async def review_submission(
    submission_id: uuid.UUID,
    review_in: SubmissionReview,
    db: AsyncSession = Depends(get_db),
):
    """Kurator/O'qituvchi o'quvchi vazifasini baholashi va izoh qoldirishi."""
    return await review_homework_submission(db, submission_id, review_in)
