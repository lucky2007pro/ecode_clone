import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from enrollments.models import Enrollment
from enrollments.schema import EnrollmentCreate


async def get_enrollments_by_user(db: AsyncSession, user_id: uuid.UUID):
    res = await db.execute(
        select(Enrollment).where(Enrollment.user_id == user_id)
    )
    return res.scalars().all()


async def get_enrollments_by_course(db: AsyncSession, course_id: uuid.UUID):
    res = await db.execute(
        select(Enrollment).where(Enrollment.course_id == course_id)
    )
    return res.scalars().all()


async def get_enrollment(db: AsyncSession, user_id: uuid.UUID, course_id: uuid.UUID):
    res = await db.execute(
        select(Enrollment)
        .where(Enrollment.user_id == user_id)
        .where(Enrollment.course_id == course_id)
    )
    return res.scalar_one_or_none()


async def create_enrollment(db: AsyncSession, enroll_in: EnrollmentCreate):
    enrollment = Enrollment(**enroll_in.model_dump())
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

async def delete_enrollment(db: AsyncSession, enrollment_id: uuid.UUID):
    res = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
    enrollment = res.scalar_one_or_none()
    if enrollment:
        await db.delete(enrollment)
        await db.commit()
        return True
    return False
