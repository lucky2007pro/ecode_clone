from sqlalchemy.ext.asyncio import AsyncSession
from courses.models import Course
from courses.schema import CourseCreate

async def create_course(db: AsyncSession, course_in: CourseCreate):
    course = Course(**course_in.model_dump())
    db.add(course)
    await db.flush()
    return course
