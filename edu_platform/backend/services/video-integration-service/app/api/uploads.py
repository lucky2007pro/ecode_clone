"""
Video yuklash uchun API Router.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import VideoAsset
from app.schemas import VideoUploadRequest, VideoUploadResponse, VideoAssetResponse
from app.kinescope_client import kinescope_client
from libs.shared_schemas.enums import VideoStatus

router = APIRouter()


@router.post("/upload-url", response_model=VideoUploadResponse, status_code=status.HTTP_201_CREATED)
async def request_upload_url(req: VideoUploadRequest, db: AsyncSession = Depends(get_db)):
    """Frontend brauzerdan Kinescope'ga to'g'ridan-to'g'ri video yuklashi uchun link beradi."""
    kinescope_res = await kinescope_client.create_video(title=req.title)

    video_asset = VideoAsset(
        lesson_id=req.lesson_id,
        kinescope_video_id=kinescope_res["kinescope_video_id"],
        upload_url=kinescope_res["upload_url"],
        status=VideoStatus.uploading,
    )
    db.add(video_asset)
    await db.flush()

    return VideoUploadResponse(
        video_id=video_asset.id,
        kinescope_video_id=kinescope_res["kinescope_video_id"],
        upload_url=kinescope_res["upload_url"],
    )
