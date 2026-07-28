from fastapi import APIRouter, HTTPException, UploadFile, File
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

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Lokal video yuklash — Kinescope sozlanmagan holatda ishlatiladi.
    Fayl ./uploads ga saqlanadi va statik URL qaytariladi.
    """
    if not (file.content_type or "").startswith("video/"):
        raise HTTPException(status_code=400, detail="Faqat video format ruxsat etilgan!")

    file_extension = (file.filename or "video.mp4").split(".")[-1]
    unique_filename = f"video_{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "video_url": f"/uploads/{unique_filename}",
        "message": "Video serverga muvaffaqiyatli yuklandi!",
    }

# Rasm, hujjat va prezentatsiya fayllari uchun umumiy endpoint
ALLOWED_ASSET_TYPES = (
    "image/",
    "application/pdf",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument",
    "application/msword",
    "text/",
)

@router.post("/upload/asset")
async def upload_asset(file: UploadFile = File(...)):
    content_type = file.content_type or ""
    if not any(content_type.startswith(t) for t in ALLOWED_ASSET_TYPES):
        raise HTTPException(status_code=400, detail="Bu fayl turi ruxsat etilmagan!")

    original = file.filename or "file"
    file_extension = original.split(".")[-1]
    unique_filename = f"asset_{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "url": f"/uploads/{unique_filename}",
        "filename": original,
    }
