"""
Kinescope.io API asinxron mijoz wrapper.
"""
import httpx
from fastapi import HTTPException

from app.core.config import settings


class KinescopeClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.KINESCOPE_API_TOKEN}",
            "Content-Type": "application/json",
        }

    async def create_video(self, title: str, filename: str = "video.mp4") -> dict:
        """
        Kinescope API'dan videoni yuklash uchun havola (Upload URL) va kinescope_video_id oladi.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Step 1: Create Video Metadata in Kinescope
            response = await client.post(
                f"{settings.KINESCOPE_API_URL}/videos",
                headers=self.headers,
                json={
                    "title": title,
                    "filename": filename,
                },
            )
            if response.status_code not in (200, 201):
                raise HTTPException(
                    status_code=500,
                    detail=f"Kinescope API bilan xatolik: {response.text}",
                )

            data = response.json().get("data", {})
            kinescope_video_id = data.get("id")

            # Step 2: Get Upload Endpoint
            upload_response = await client.post(
                settings.KINESCOPE_UPLOADER_URL,
                headers={
                    "X-Video-Id": kinescope_video_id,
                    "X-Video-Title": title,
                    "Authorization": f"Bearer {settings.KINESCOPE_API_TOKEN}",
                },
            )
            upload_url = (
                upload_response.headers.get("Location")
                or f"https://uploader.kinescope.io/v2/video/{kinescope_video_id}"
            )

            return {
                "kinescope_video_id": kinescope_video_id,
                "upload_url": upload_url,
            }


kinescope_client = KinescopeClient()
