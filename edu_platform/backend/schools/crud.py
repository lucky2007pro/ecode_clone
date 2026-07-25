from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schools.models import School
from schools.schema import SchoolCreate

async def create_school(db: AsyncSession, school_in: SchoolCreate):
    school = School(**school_in.model_dump())
    db.add(school)
    await db.flush()
    return school
