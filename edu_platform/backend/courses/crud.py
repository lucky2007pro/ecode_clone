from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from courses.models import Course
from courses.schema import CourseCreate

from sqlalchemy import func
from lessons.models import Lesson

async def get_courses(db: AsyncSession):
    res = await db.execute(select(Course))
    courses = res.scalars().all()
    
    # Har bir kurs uchun darslar sonini hisoblaymiz (sodda usul)
    for c in courses:
        count_res = await db.execute(select(func.count(Lesson.id)).where(Lesson.course_id == c.id))
        c.lessons_count = count_res.scalar()
        
    return courses

async def create_course(db: AsyncSession, course_in: CourseCreate):
    course = Course(**course_in.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course
