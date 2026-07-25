"""
video-integration-service Pydantic sxemalari.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from libs.shared_schemas.enums import VideoStatus


class VideoUploadRequest(BaseModel):
    lesson_id: uuid.UUID
    title: str


class VideoUploadResponse(BaseModel):
    video_id: uuid.UUID
    kinescope_video_id: str
    upload_url: str


class KinescopeWebhookEvent(BaseModel):
    event: str  # e.g. "video.ready", "video.processing"
    data: dict


class VideoAssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lesson_id: uuid.UUID
    kinescope_video_id: str | None
    upload_url: str | None
    status: VideoStatus
    duration_seconds: int | None
    error_message: str | None
    created_at: datetime
