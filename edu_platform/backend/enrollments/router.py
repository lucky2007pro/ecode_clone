import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from enrollments.schema import EnrollmentCreate, EnrollmentResponse
from enrollments.crud import get_enrollments_by_user, get_enrollments_by_course, get_enrollment, create_enrollment
from courses.crud import get_courses
from users.crud import get_user_by_email
from permissions.dependencies import get_current_school_id

router = APIRouter()


@router.get("/user/{user_id}", response_model=List[EnrollmentResponse])
async def list_user_enrollments(user_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):
    """Foydalanuvchining barcha kursga yozilishlari."""
    return await get_enrollments_by_user(db, user_id, school_id)


@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])
async def list_course_enrollments(course_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):
    """Kursga yozilgan barcha studentlar."""
    return await get_enrollments_by_course(db, course_id, school_id)


from users.models import User
from courses.models import Course
from payments.models import Transaction, TransactionType
from permissions.dependencies import get_current_user, get_current_school_id

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_user(
    enroll_in: EnrollmentCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    school_id=Depends(get_current_school_id)
):
    """Foydalanuvchini kursga yozish (bonus balansdan kamaytiriladi)."""
    # Tekshirish: allaqachon yozilganmi
    existing = await get_enrollment(db, enroll_in.user_id, enroll_in.course_id)
    if existing:
        raise HTTPException(status_code=400, detail="Foydalanuvchi allaqachon bu kursga yozilgan")
        
    # Get user and course
    user_res = await db.execute(select(User).where(User.id == enroll_in.user_id))
    user = user_res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
        
    course_res = await db.execute(select(Course).where(Course.id == enroll_in.course_id).where(Course.school_id == school_id))
    course = course_res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi")
        
    # To'lovni yechish: Faqat o'quvchi o'zi sotib olayotgan bo'lsa
    # Agar admin / manager / o'qituvchi biriktirayotgan bo'lsa, to'lov yechilmaydi.
    if user.role.value == "student" and current_user.role.value == "student":
        course_price = course.price or 0.0
        if user.balance < course_price:
            raise HTTPException(status_code=400, detail="Balansda yetarli mablag' mavjud emas")
            
        user.balance -= course_price
        db.add(user)
        
        transaction = Transaction(
            user_id=user.id,
            amount=course_price,
            type=TransactionType.OUT,
            description=f"Kurs xaridi: {course.title}"
        )
        db.add(transaction)
        
    return await create_enrollment(db, enroll_in, school_id)

from enrollments.crud import delete_enrollment

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll_user(enrollment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Foydalanuvchini kursdan o'chirish."""
    success = await delete_enrollment(db, enrollment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Yozilish topilmadi")
    return None
