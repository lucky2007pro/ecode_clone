from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schools.schema import SchoolCreate, SchoolResponse
from schools.crud import create_school

router = APIRouter()

@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def add_school(school_in: SchoolCreate, db: AsyncSession = Depends(get_db)):
    return await create_school(db, school_in)
