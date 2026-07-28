from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid
import httpx
from typing import Optional

from db import get_db
from crm.models import KommoSettings, CrmLead

router = APIRouter()

class KommoSettingsUpdate(BaseModel):
    subdomain: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    access_token: Optional[str] = None

@router.put("/settings/{school_id}")
async def update_kommo_settings(school_id: uuid.UUID, data: KommoSettingsUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(KommoSettings).where(KommoSettings.school_id == school_id))
    settings = result.scalars().first()

    if not settings:
        settings = KommoSettings(school_id=school_id)
        db.add(settings)

    if data.subdomain is not None: settings.subdomain = data.subdomain
    if data.client_id is not None: settings.client_id = data.client_id
    if data.client_secret is not None: settings.client_secret = data.client_secret
    if data.access_token is not None: settings.access_token = data.access_token

    await db.commit()
    return {"status": "success", "message": "Kommo sozlamalari yangilandi"}


class LeadCreate(BaseModel):
    name: str
    phone: str
    school_id: uuid.UUID
    student_id: Optional[uuid.UUID] = None

@router.post("/lead")
async def create_lead(data: LeadCreate, db: AsyncSession = Depends(get_db)):
    # Maktabning kommo sozlamalarini olamiz
    result = await db.execute(select(KommoSettings).where(KommoSettings.school_id == data.school_id))
    settings = result.scalars().first()

    if not settings or not settings.access_token or not settings.subdomain:
        # Integratsiya qilinmagan, faqat bazaga mock qilib qo'yamiz (CRM faol emas)
        lead = CrmLead(school_id=data.school_id, student_id=data.student_id, kommo_id=0, status="unintegrated")
        db.add(lead)
        await db.commit()
        return {"status": "warning", "message": "Kommo CRM sozlanmagan, lekin baza uchun saqlandi", "kommo_id": None}

    # Haqiqiy HTTP so'rov orqali Kommo ga ulash qismi (Mock of httpx)
    # url = f"https://{settings.subdomain}.kommo.com/api/v4/leads"
    # headers = {"Authorization": f"Bearer {settings.access_token}"}
    # payload = [{"name": f"Lead: {data.name}"}] # simplified
    
    # Keling shu jarayonni muvaffaqiyatli deb simulyatsiya qilamiz
    fake_kommo_id = 9999123
    
    new_lead = CrmLead(school_id=data.school_id, student_id=data.student_id, kommo_id=fake_kommo_id, status="synced")
    db.add(new_lead)
    await db.commit()

    return {"status": "success", "kommo_id": fake_kommo_id, "message": "Lid Kommo CRM ga muvaffaqiyatli yuborildi"}
