import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from lessons.models import Lesson, CourseModule

from courses.models import Course

from lessons.schema import LessonCreate, CourseModuleCreate

async def get_modules_by_course(db: AsyncSession, course_id: uuid.UUID, school_id):

    res = await db.execute(

        select(CourseModule)

        .where(CourseModule.course_id == course_id)

        .where(CourseModule.school_id == school_id)

        .order_by(CourseModule.order)

    )

    return res.scalars().all()

async def create_module(db: AsyncSession, module_in: CourseModuleCreate, school_id):

    course_res = await db.execute(select(Course).where(Course.id == module_in.course_id).where(Course.school_id == school_id))

    if not course_res.scalar_one_or_none():

        return None

    module = CourseModule(**module_in.model_dump(), school_id=school_id)

    db.add(module)

    await db.commit()

    await db.refresh(module)

    return module

async def get_lessons_by_course(db: AsyncSession, course_id: uuid.UUID, school_id):

    res = await db.execute(

        select(Lesson)

        .where(Lesson.course_id == course_id)

        .where(Lesson.school_id == school_id)

        .order_by(Lesson.order)

    )

    return res.scalars().all()

async def get_lesson_by_id(db: AsyncSession, lesson_id: uuid.UUID, school_id=None):

    query = select(Lesson).where(Lesson.id == lesson_id)

    if school_id is not None: query = query.where(Lesson.school_id == school_id)

    res = await db.execute(query)

    return res.scalar_one_or_none()

async def create_lesson(db: AsyncSession, lesson_in: LessonCreate, school_id):

    course_res = await db.execute(select(Course).where(Course.id == lesson_in.course_id).where(Course.school_id == school_id))

    if not course_res.scalar_one_or_none():

        return None

    lesson = Lesson(**lesson_in.model_dump(), school_id=school_id)

    db.add(lesson)

    await db.commit()

    await db.refresh(lesson)

    return lesson

async def update_lesson(db: AsyncSession, lesson_id: uuid.UUID, lesson_in: LessonCreate, school_id):

    lesson = await get_lesson_by_id(db, lesson_id, school_id)

    if not lesson:

        return None

    for key, value in lesson_in.model_dump().items():

        setattr(lesson, key, value)

    await db.commit()

    await db.refresh(lesson)

    return lesson

async def delete_lesson(db: AsyncSession, lesson_id: uuid.UUID, school_id):

    lesson = await get_lesson_by_id(db, lesson_id, school_id)

    if lesson:

        await db.delete(lesson)

        await db.commit()

    return lesson

