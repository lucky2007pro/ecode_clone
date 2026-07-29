from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from courses.models import Course

from courses.schema import CourseCreate

from sqlalchemy import func

from lessons.models import Lesson

async def get_courses(db: AsyncSession, school_id):

    res = await db.execute(select(Course).where(Course.school_id == school_id))

    courses = res.scalars().all()

    for c in courses:

        count_res = await db.execute(select(func.count(Lesson.id)).where(Lesson.course_id == c.id))

        c.lessons_count = count_res.scalar()

    return courses

async def get_course(db: AsyncSession, course_id, school_id):

    res = await db.execute(select(Course).where(Course.id == course_id, Course.school_id == school_id))

    course = res.scalar_one_or_none()

    if course:

        count_res = await db.execute(select(func.count(Lesson.id)).where(Lesson.course_id == course_id))

        course.lessons_count = count_res.scalar()

    return course

async def create_course(db: AsyncSession, course_in: CourseCreate, school_id, teacher_id=None):

    course = Course(**course_in.model_dump(), school_id=school_id, teacher_id=teacher_id)

    db.add(course)

    await db.commit()

    await db.refresh(course)

    return course

