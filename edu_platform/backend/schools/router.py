from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from db import get_db
from schools.schema import SchoolCreate, SchoolResponse
from schools.crud import create_school
from schools.models import UserSchool, MembershipStatus, School
from users.models import User
from users.schema import UserCreate
from users.crud import get_user_by_email, create_user
from schools.crud import create_user_school
import uuid

router = APIRouter()

from permissions.dependencies import get_current_user_school_id

@router.get("/my", response_model=SchoolResponse)
async def get_my_school(school_id: str = Depends(get_current_user_school_id), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(School).where(School.id == uuid.UUID(school_id)))
    school = res.scalar_one_or_none()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def add_school(school_in: SchoolCreate, owner_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await create_school(db, school_in.name, school_in.subdomain, owner_id)

@router.get("/{school_id}/users")
async def get_school_users(school_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(User.id, User.full_name, User.email, User.role)
        .join(UserSchool, User.id == UserSchool.user_id)
        .where(UserSchool.school_id == school_id)
        .where(UserSchool.status == MembershipStatus.APPROVED)
    )
    users = res.all()
    return [{"id": u.id, "full_name": u.full_name, "email": u.email, "role": u.role} for u in users]

@router.post("/{school_id}/users", status_code=status.HTTP_201_CREATED)
async def add_school_user(school_id: uuid.UUID, user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Bunday email allaqachon mavjud")
    
    new_user = await create_user(db, user_in)
    await create_user_school(db, new_user.id, school_id, MembershipStatus.APPROVED)
    return {"id": new_user.id, "full_name": new_user.full_name, "email": new_user.email, "role": new_user.role}

@router.get("/{school_id}/pending-users")
async def get_pending_users(school_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(User.id, User.full_name, User.email, User.role)
        .join(UserSchool, User.id == UserSchool.user_id)
        .where(UserSchool.school_id == school_id)
        .where(UserSchool.status == MembershipStatus.PENDING)
    )
    users = res.all()
    return [{"id": u.id, "full_name": u.full_name, "email": u.email, "role": u.role} for u in users]

@router.post("/{school_id}/approve/{user_id}")
async def approve_user(school_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        update(UserSchool)
        .where(UserSchool.school_id == school_id)
        .where(UserSchool.user_id == user_id)
        .values(status=MembershipStatus.APPROVED)
    )
    await db.commit()
    return {"message": "User approved successfully"}

from pydantic import BaseModel
from typing import Optional

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    custom_domain: Optional[str] = None
    primary_color: Optional[str] = None

@router.put("/{school_id}")
async def update_school(school_id: uuid.UUID, school_in: SchoolUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(School).where(School.id == school_id))
    school = res.scalar_one_or_none()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    if school_in.name:
        school.name = school_in.name
    if school_in.custom_domain:
        school.custom_domain = school_in.custom_domain
    if school_in.primary_color:
        school.primary_color = school_in.primary_color
        
    await db.commit()
    await db.refresh(school)
    return school
