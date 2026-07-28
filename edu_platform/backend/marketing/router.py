from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid
from typing import Optional

from db import get_db
from marketing.models import MarketingSettings

router = APIRouter()

class MarketingUpdate(BaseModel):
    facebook_pixel_id: Optional[str] = None
    google_analytics_id: Optional[str] = None
    yandex_metrika_id: Optional[str] = None

@router.get("/{school_id}")
async def get_marketing_settings(school_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(MarketingSettings).where(MarketingSettings.school_id == school_id))
    settings = res.scalar_one_or_none()
    if not settings:
        # Create default
        settings = MarketingSettings(school_id=school_id)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
    
    return {
        "facebook_pixel_id": settings.facebook_pixel_id,
        "google_analytics_id": settings.google_analytics_id,
        "yandex_metrika_id": settings.yandex_metrika_id
    }

@router.put("/{school_id}")
async def update_marketing_settings(school_id: uuid.UUID, data: MarketingUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(MarketingSettings).where(MarketingSettings.school_id == school_id))
    settings = res.scalar_one_or_none()
    if not settings:
        settings = MarketingSettings(school_id=school_id)
        db.add(settings)
    
    if data.facebook_pixel_id is not None:
        settings.facebook_pixel_id = data.facebook_pixel_id
    if data.google_analytics_id is not None:
        settings.google_analytics_id = data.google_analytics_id
    if data.yandex_metrika_id is not None:
        settings.yandex_metrika_id = data.yandex_metrika_id
        
    await db.commit()
    return {"message": "Marketing settings updated"}
