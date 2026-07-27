from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from courses.models import Course
from courses.schema import CourseCreate

async def get_courses(db: AsyncSession):
    res = await db.execute(select(Course))
    return res.scalars().all()

async def create_course(db: AsyncSession, course_in: CourseCreate):
    course = Course(**course_in.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course
