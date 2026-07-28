import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from enrollments.schema import EnrollmentCreate, EnrollmentResponse
from enrollments.crud import get_enrollments_by_user, get_enrollments_by_course, get_enrollment, create_enrollment
from courses.crud import get_courses
from users.crud import get_user_by_email

router = APIRouter()


@router.get("/user/{user_id}", response_model=List[EnrollmentResponse])
async def list_user_enrollments(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Foydalanuvchining barcha kursga yozilishlari."""
    return await get_enrollments_by_user(db, user_id)


@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])
async def list_course_enrollments(course_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Kursga yozilgan barcha studentlar."""
    return await get_enrollments_by_course(db, course_id)


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_user(enroll_in: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    """Foydalanuvchini kursga yozish (bonus balansdan kamaytiriladi)."""
    # Tekshirish: allaqachon yozilganmi
    existing = await get_enrollment(db, enroll_in.user_id, enroll_in.course_id)
    if existing:
        raise HTTPException(status_code=400, detail="Foydalanuvchi allaqachon bu kursga yozilgan")
    return await create_enrollment(db, enroll_in)

from enrollments.crud import delete_enrollment

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll_user(enrollment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Foydalanuvchini kursdan o'chirish."""
    success = await delete_enrollment(db, enrollment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Yozilish topilmadi")
    return None
