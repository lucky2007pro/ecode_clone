import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from lessons.models import Lesson
from lessons.schema import LessonCreate


async def get_lessons_by_course(db: AsyncSession, course_id: uuid.UUID):
    res = await db.execute(
        select(Lesson)
        .where(Lesson.course_id == course_id)
        .order_by(Lesson.order)
    )
    return res.scalars().all()


async def get_lesson_by_id(db: AsyncSession, lesson_id: uuid.UUID):
    res = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    return res.scalar_one_or_none()


async def create_lesson(db: AsyncSession, lesson_in: LessonCreate):
    lesson = Lesson(**lesson_in.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def update_lesson(db: AsyncSession, lesson_id: uuid.UUID, lesson_in: LessonCreate):
    lesson = await get_lesson_by_id(db, lesson_id)
    if not lesson:
        return None
    for key, value in lesson_in.model_dump().items():
        setattr(lesson, key, value)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def delete_lesson(db: AsyncSession, lesson_id: uuid.UUID):
    lesson = await get_lesson_by_id(db, lesson_id)
    if lesson:
        await db.delete(lesson)
        await db.commit()
    return lesson
