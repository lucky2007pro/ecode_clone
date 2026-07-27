from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schools.models import School, UserSchool
from schools.schema import SchoolCreate
import uuid

async def get_school_by_subdomain(db: AsyncSession, subdomain: str):
    res = await db.execute(select(School).where(School.subdomain == subdomain))
    return res.scalars().first()

async def create_school(db: AsyncSession, name: str, subdomain: str, owner_id: uuid.UUID):
    school = School(name=name, subdomain=subdomain, owner_id=owner_id)
    db.add(school)
    await db.flush()
    return school

async def create_user_school(db: AsyncSession, user_id: uuid.UUID, school_id: uuid.UUID, status: str = "pending"):
    us = UserSchool(user_id=user_id, school_id=school_id, status=status)
    db.add(us)
    await db.flush()
    return us
