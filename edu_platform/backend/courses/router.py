from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from courses.schema import CourseCreate, CourseResponse
from courses.crud import create_course, get_courses
from permissions.dependencies import RequirePermissions
from permissions.enums import Permission

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db), _=Depends(RequirePermissions([Permission.VIEW_COURSES]))):
    return await get_courses(db)

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def add_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db), _=Depends(RequirePermissions([Permission.MANAGE_COURSES]))):
    return await create_course(db, course_in)
