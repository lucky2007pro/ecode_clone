import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from courses.schema import CourseCreate, CourseResponse
from courses.crud import create_course, get_courses, get_course
from permissions.dependencies import RequirePermissions, get_current_school_id, get_current_user
from permissions.enums import Permission, Role

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id), _=Depends(RequirePermissions([Permission.VIEW_COURSES]))):
    return await get_courses(db, school_id)

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course_detail(course_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id), _=Depends(RequirePermissions([Permission.VIEW_COURSES]))):
    course = await get_course(db, course_id, school_id)
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi")
    return course

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def add_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id), current_user=Depends(get_current_user), _=Depends(RequirePermissions([Permission.MANAGE_COURSES]))):
    # Kursni teacher yaratganda unga biriktiramiz (admin yaratganda teacher_id bo'sh qoladi)
    teacher_id = current_user.id if current_user.role == Role.TEACHER else None
    return await create_course(db, course_in, school_id, teacher_id=teacher_id)
