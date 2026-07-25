from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from courses.schema import CourseCreate, CourseResponse
from courses.crud import create_course

router = APIRouter()

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def add_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db)):
    return await create_course(db, course_in)
