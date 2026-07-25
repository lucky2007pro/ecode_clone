"""
course-service RabbitMQ event consumer'lari.
video.ready eventini eshitib, tegishli darsga kinescope_video_id yozadi.
"""
import uuid
import logging
from sqlalchemy import select
from app.core.database import async_session_maker
from app.models import Lesson

logger = logging.getLogger("course_event_consumer")


async def handle_video_ready_event(payload: dict):
    """video.ready hodisasi kelganda ishlaydi."""
    data = payload.get("payload", {})
    lesson_id_str = data.get("lesson_id")
    kinescope_video_id = data.get("kinescope_video_id")

    if not lesson_id_str or not kinescope_video_id:
        return

    async with async_session_maker() as db:
        try:
            lesson_id = uuid.UUID(lesson_id_str)
            stmt = select(Lesson).where(Lesson.id == lesson_id)
            res = await db.execute(stmt)
            lesson = res.scalar_one_or_none()

            if lesson:
                lesson.kinescope_video_id = kinescope_video_id
                await db.commit()
                logger.info(f"Lesson '{lesson.id}' ga Kinescope Video ID '{kinescope_video_id}' biriktirildi.")
        except Exception as e:
            await db.rollback()
            logger.error(f"Lesson yangilashda xatolik: {e}")
