import uuid

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from db import get_db

from enrollments.schema import EnrollmentCreate, EnrollmentResponse, PurchaseRequest

from enrollments.crud import (

    get_enrollments_by_user,

    get_enrollments_by_course,

    get_enrollment,

    create_enrollment,

    delete_enrollment,

)

from users.models import User

from courses.models import Course

from permissions.dependencies import get_current_user, get_current_school_id

from permissions.enums import Role

from payments.models import Transaction, TransactionType

from notifications.crud import create_notification, get_school_admin_ids

router = APIRouter()

@router.get("/user/{user_id}", response_model=List[EnrollmentResponse])

async def list_user_enrollments(user_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Foydalanuvchining barcha kursga yozilishlari."""

    return await get_enrollments_by_user(db, user_id, school_id)

@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])

async def list_course_enrollments(course_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Kursga yozilgan barcha studentlar."""

    return await get_enrollments_by_course(db, course_id, school_id)

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)

async def enroll_user(

    enroll_in: EnrollmentCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(get_current_user),

    school_id=Depends(get_current_school_id),

):

    """Foydalanuvchini kursga yozish (bepul — admin biriktiradi yoki student o'zi yoziladi)."""

    existing = await get_enrollment(db, enroll_in.user_id, enroll_in.course_id)

    if existing:

        raise HTTPException(status_code=400, detail="Foydalanuvchi allaqachon bu kursga yozilgan")

    user_res = await db.execute(select(User).where(User.id == enroll_in.user_id))

    if not user_res.scalar_one_or_none():

        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    course_res = await db.execute(select(Course).where(Course.id == enroll_in.course_id).where(Course.school_id == school_id))

    if not course_res.scalar_one_or_none():

        raise HTTPException(status_code=404, detail="Kurs topilmadi")

    return await create_enrollment(db, enroll_in, school_id)

@router.post("/purchase", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)

async def purchase_course(

    req: PurchaseRequest,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(get_current_user),

    school_id=Depends(get_current_school_id),

):

    """O'quvchi kursni o'z balansidan sotib oladi. Admin/teacher POST / ishlatadi."""

    role = current_user.role if isinstance(current_user.role, Role) else Role(current_user.role)

    if role != Role.STUDENT:

        raise HTTPException(status_code=400, detail="Faqat o'quvchilar kurs sotib olishi mumkin. Xodimlar POST / dan foydalanadi.")

    course_res = await db.execute(select(Course).where(Course.id == req.course_id).where(Course.school_id == school_id))

    course = course_res.scalar_one_or_none()

    if not course:

        raise HTTPException(status_code=404, detail="Kurs topilmadi")

    existing = await get_enrollment(db, current_user.id, req.course_id)

    if existing:

        raise HTTPException(status_code=400, detail="Siz allaqachon bu kursga yozilgansiz")

    price = float(course.price or 0)

    if price > 0:

        if float(current_user.balance) < price:

            raise HTTPException(

                status_code=400,

                detail=f"Balans yetarli emas. Kerak: {price:,.0f} UZS, mavjud: {float(current_user.balance):,.0f} UZS"

            )

        current_user.balance = float(current_user.balance) - price

        db.add(Transaction(

            user_id=current_user.id, school_id=school_id, amount=price,

            type=TransactionType.OUT, description=f"Kurs sotib olindi: {course.title}"

        ))

    enrollment = await create_enrollment(db, EnrollmentCreate(user_id=current_user.id, course_id=req.course_id), school_id)

    if price > 0:

        for admin_id in await get_school_admin_ids(db, school_id):

            await create_notification(

                db, admin_id, school_id,

                "Kurs sotib olindi",

                f"{current_user.full_name} \"{course.title}\" kursini {price:,.0f} UZS ga sotib oldi"

            )

        await create_notification(

            db, current_user.id, school_id,

            "Kurs sotib olindi",

            f"Siz \"{course.title}\" kursini {price:,.0f} UZS ga sotib oldingiz"

        )

    return enrollment

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)

async def unenroll_user(

    enrollment_id: uuid.UUID,

    db: AsyncSession = Depends(get_db),

    school_id=Depends(get_current_school_id),

):

    """Foydalanuvchini kursdan o'chirish (faqat o'z maktabidagi yozilishlarni)."""

    success = await delete_enrollment(db, enrollment_id, school_id)

    if not success:

        raise HTTPException(status_code=404, detail="Yozilish topilmadi")

    return None

