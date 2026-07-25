"""
Progress & Certificate API Router.
"""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import LessonProgress, Certificate
from app.schemas import LessonProgressUpdate, LessonProgressResponse, CertificateResponse

router = APIRouter()


@router.post("/complete", response_model=LessonProgressResponse, status_code=status.HTTP_200_OK)
async def complete_lesson(
    req: LessonProgressUpdate,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Darsni tugatildi deb belgilash."""
    stmt = select(LessonProgress).where(
        LessonProgress.user_id == user_id,
        LessonProgress.lesson_id == req.lesson_id,
    )
    res = await db.execute(stmt)
    progress = res.scalar_one_or_none()

    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            course_id=req.course_id,
            lesson_id=req.lesson_id,
            is_completed=True,
            completed_at=datetime.now(timezone.utc),
        )
        db.add(progress)
    else:
        progress.is_completed = req.is_completed
        if req.is_completed:
            progress.completed_at = datetime.now(timezone.utc)

    await db.flush()
    return progress


@router.get("/certificate/{course_id}", response_model=CertificateResponse)
async def get_certificate(
    course_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Kursni bitirgach o'quvchi sertifikatini ko'rish yoki generatsiya qilish."""
    stmt = select(Certificate).where(
        Certificate.user_id == user_id,
        Certificate.course_id == course_id,
    )
    res = await db.execute(stmt)
    cert = res.scalar_one_or_none()

    if not cert:
        # Avto Sertifikat Generatsiya qilamiz
        cert_no = f"EXODE-{uuid.uuid4().hex[:8].upper()}"
        cert = Certificate(
            user_id=user_id,
            course_id=course_id,
            certificate_number=cert_no,
            file_url=f"https://api.exode.biz/certificates/{cert_no}.pdf",
        )
        db.add(cert)
        await db.flush()

    return cert
