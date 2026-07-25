"""
Enrollments API Router.
"""
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import EnrollmentCreate, EnrollmentResponse
from app.services.course_service import enroll_user, get_user_enrollments

router = APIRouter()


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def new_enrollment(enroll_in: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    """O'quvchini kursga biriktirish (Enrollment)."""
    return await enroll_user(db, enroll_in)


@router.get("/user/{user_id}", response_model=list[EnrollmentResponse])
async def list_user_enrollments(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """O'quvchining barcha a'zo bo'lgan kurslari."""
    return await get_user_enrollments(db, user_id)
