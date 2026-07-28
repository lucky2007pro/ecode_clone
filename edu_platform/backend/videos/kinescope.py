import os
import httpx
from dotenv import load_dotenv

load_dotenv()

KINESCOPE_API_KEY = os.getenv("KINESCOPE_API_KEY", "")
KINESCOPE_PROJECT_ID = os.getenv("KINESCOPE_PROJECT_ID", "")
KINESCOPE_INIT_URL = "https://uploader.kinescope.io/v2/init"

async def init_video_upload(filename: str, title: str, filesize: int):
    if not KINESCOPE_API_KEY:
        raise RuntimeError("KINESCOPE_API_KEY sozlanmagan")
    if not KINESCOPE_PROJECT_ID:
        raise RuntimeError("KINESCOPE_PROJECT_ID sozlanmagan")

    payload = {
        "parent_id": KINESCOPE_PROJECT_ID,
        "type": "video",
        "filename": filename,
        "title": title or filename,
        "filesize": filesize,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            KINESCOPE_INIT_URL,
            json=payload,
            headers={"Authorization": f"Bearer {KINESCOPE_API_KEY}"},
        )
    if response.status_code not in (200, 201):
        raise RuntimeError(f"Kinescope upload init xatosi: {response.status_code} {response.text[:500]}")
    data = response.json().get("data", response.json())
    return {"upload_url": data["endpoint"], "video_id": data.get("id")}
