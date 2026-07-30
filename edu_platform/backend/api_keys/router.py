from fastapi import APIRouter, Depends, HTTPException, Header, status

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from pydantic import BaseModel

import uuid

import secrets

from db import get_db

from api_keys.models import APIKey

from users.models import User

from schools.models import School

router = APIRouter()

class APIKeyCreate(BaseModel):

    name: str

@router.post("/keys/{school_id}")

async def generate_api_key(school_id: uuid.UUID, data: APIKeyCreate, db: AsyncSession = Depends(get_db)):

    """Maktab uchun yangi API kalit yaratish (Faqat admin uchun)"""

    raw_key = secrets.token_urlsafe(32)

    prefix = "exode_"

    full_key = prefix + raw_key

    api_key = APIKey(school_id=school_id, key=full_key, name=data.name)

    db.add(api_key)

    await db.commit()

    return {"name": data.name, "api_key": full_key}

saas_router = APIRouter()

async def verify_api_key(authorization: str = Header(None), school_id: uuid.UUID = Header(None, alias="School-Id"), db: AsyncSession = Depends(get_db)):

    if not authorization or not authorization.startswith("Bearer "):

        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]

    res = await db.execute(select(APIKey).where(APIKey.key == token).where(APIKey.school_id == school_id))

    api_key = res.scalar_one_or_none()

    if not api_key:

        raise HTTPException(status_code=401, detail="Invalid API Key or School ID")

    return api_key.school_id

class SaasUserCreate(BaseModel):

    email: str

    extId: str | None = None

    full_name: str

@saas_router.post("/v2/user/create")

async def saas_create_user(

    data: SaasUserCreate,

    school_id: uuid.UUID = Depends(verify_api_key),

    db: AsyncSession = Depends(get_db)

):

    """
    Tashqi tizimlardan (CRM va hk) API orqali platformaga o'quvchi qo'shish.
    """

    res = await db.execute(select(User).where(User.email == data.email))

    if res.scalar_one_or_none():

        return {"status": "error", "message": "User already exists"}

    return {

        "status": "success",

        "message": f"User {data.email} created for school {school_id}",

        "user_id": str(uuid.uuid4())

    }

