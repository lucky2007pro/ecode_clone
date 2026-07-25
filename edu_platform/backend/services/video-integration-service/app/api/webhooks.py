"""
Kinescope Webhook router.
Kinescope video kodlashni tugatgach shu yerga POST so'rov yuboradi.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import VideoAsset
from app.events.publishers import publish_video_ready
from libs.shared_schemas.enums import VideoStatus

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def handle_kinescope_webhook(payload: dict, db: AsyncSession = Depends(get_db)):
    """Kinescope status o'zgarishi bo'yicha webhook qabul qiladi."""
    event_type = payload.get("event") or payload.get("type")
    data = payload.get("data", {})
    kinescope_video_id = data.get("id") or data.get("video_id")

    if not kinescope_video_id:
        return {"status": "ignored", "reason": "No video_id"}

    stmt = select(VideoAsset).where(VideoAsset.kinescope_video_id == kinescope_video_id)
    res = await db.execute(stmt)
    video_asset = res.scalar_one_or_none()

    if not video_asset:
        return {"status": "ignored", "reason": "VideoAsset not found"}

    if event_type in ("video.ready", "video.processed"):
        video_asset.status = VideoStatus.ready
        video_asset.duration_seconds = data.get("duration", 0)

        # Eventni RabbitMQ'ga yuborish (course-service tinglaydi va Lesson.kinescope_video_id ga yozadi)
        await publish_video_ready(
            lesson_id=str(video_asset.lesson_id),
            kinescope_video_id=video_asset.kinescope_video_id,
            duration_seconds=video_asset.duration_seconds,
        )

    elif event_type == "video.error":
        video_asset.status = VideoStatus.error
        video_asset.error_message = data.get("error", "Transcoding error")

    return {"status": "ok"}
