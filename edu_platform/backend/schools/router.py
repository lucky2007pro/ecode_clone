from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from db import get_db
from schools.schema import SchoolCreate, SchoolResponse
from schools.crud import create_school
from schools.models import UserSchool, MembershipStatus, School
from users.models import User
import uuid

router = APIRouter()

@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def add_school(school_in: SchoolCreate, owner_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await create_school(db, school_in.name, school_in.subdomain, owner_id)

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
