from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid
from typing import Optional

from db import get_db
from bot.models import TelegramBotSettings
from permissions.dependencies import get_current_school_id

router = APIRouter()

class BotUpdate(BaseModel):
    bot_token: Optional[str] = None
    private_channel_id: Optional[str] = None
    invite_link: Optional[str] = None

@router.get("/{school_id}")
async def get_bot_settings(school_id: uuid.UUID, db: AsyncSession = Depends(get_db), token_school_id=Depends(get_current_school_id)):
    if school_id != token_school_id: raise HTTPException(status_code=403, detail="Boshqa maktabga kirish taqiqlangan")
    res = await db.execute(select(TelegramBotSettings).where(TelegramBotSettings.school_id == school_id))
    settings = res.scalar_one_or_none()
    if not settings:
        settings = TelegramBotSettings(school_id=school_id)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
        
    return {
        "bot_token": settings.bot_token,
        "private_channel_id": settings.private_channel_id,
        "invite_link": settings.invite_link
    }

@router.put("/{school_id}")
async def update_bot_settings(school_id: uuid.UUID, data: BotUpdate, db: AsyncSession = Depends(get_db), token_school_id=Depends(get_current_school_id)):
    if school_id != token_school_id: raise HTTPException(status_code=403, detail="Boshqa maktabga kirish taqiqlangan")
    res = await db.execute(select(TelegramBotSettings).where(TelegramBotSettings.school_id == school_id))
    settings = res.scalar_one_or_none()
    if not settings:
        settings = TelegramBotSettings(school_id=school_id)
        db.add(settings)
        
    if data.bot_token is not None:
        settings.bot_token = data.bot_token
    if data.private_channel_id is not None:
        settings.private_channel_id = data.private_channel_id
    if data.invite_link is not None:
        settings.invite_link = data.invite_link
        
    await db.commit()
    return {"message": "Telegram Bot settings updated"}

@router.post("/{school_id}/get-invite")
async def get_channel_invite(school_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """O'quvchi to'lov qilgach, unga beriladigan avto link."""
    res = await db.execute(select(TelegramBotSettings).where(TelegramBotSettings.school_id == school_id))
    settings = res.scalar_one_or_none()
    
    if not settings or not settings.invite_link:
        return {"error": "Kanalga havola sozlanmagan"}
        
    return {"invite_link": settings.invite_link}
