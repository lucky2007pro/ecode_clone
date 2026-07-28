from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from videos.kinescope import init_video_upload
import uuid
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class VideoUploadInit(BaseModel):
    filename: str
    title: str | None = None
    filesize: int

@router.post("/upload/init")
async def upload_video_init(data: VideoUploadInit):
    try:
        return await init_video_upload(data.filename, data.title or data.filename, data.filesize)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

''' Legacy local upload endpoint kept disabled in favor of direct Tus upload to Kinescope.
@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Kinescope ga video yuklash (Hozircha lokal saqlanib, Kinescope API mock qilinadi).
    Kelajakda httpx orqali Kinescope ga jo'natiladi.
    """
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Faqat video format ruxsat etilgan!")

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"kinescope_{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Fake Kinescope URL qaytaramiz (aslida backenddagi lokal URL)
    # Agar frontend localhost:8000 da ishlayotgan bo'lsa
    video_url = f"http://localhost:8000/uploads/{unique_filename}"
    
    return {
        "status": "success", 
        "kinescope_id": unique_filename,
        "video_url": video_url,
        "message": "Video Kinescope (simulated) serveriga muvaffaqiyatli yuklandi!"
    }
'''
