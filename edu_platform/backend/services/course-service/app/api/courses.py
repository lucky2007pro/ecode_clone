"""
Courses API Router.
"""
import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import CourseCreate, CourseUpdate, CourseResponse
from app.services.course_service import (
    create_course,
    get_courses_by_school,
    get_course_by_id,
    update_course,
)

router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_new_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db)):
    """Yangi kurs yaratish."""
    return await create_course(db, course_in)


@router.get("/school/{school_id}", response_model=list[CourseResponse])
async def list_courses_by_school(
    school_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Maktabga tegishli barcha kurslarni olish."""
    return await get_courses_by_school(db, school_id, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Kursni to'liq modullari va darslari bilan olish."""
    return await get_course_by_id(db, course_id)


@router.patch("/{course_id}", response_model=CourseResponse)
async def patch_course(
    course_id: uuid.UUID,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Kurs ma'lumotlarini tahrirlash."""
    return await update_course(db, course_id, course_update)
