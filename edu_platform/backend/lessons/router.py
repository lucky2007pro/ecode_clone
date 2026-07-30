import uuid

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

from lessons.schema import LessonCreate, LessonResponse, CourseModuleCreate, CourseModuleResponse

from lessons.crud import get_lessons_by_course, get_lesson_by_id, create_lesson, update_lesson, delete_lesson, get_modules_by_course, create_module

from permissions.dependencies import RequirePermissions, get_current_school_id

from permissions.enums import Permission

router = APIRouter()

@router.get("/course/{course_id}/modules", response_model=List[CourseModuleResponse])

async def list_modules(course_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    return await get_modules_by_course(db, course_id, school_id)

@router.post("/modules", response_model=CourseModuleResponse, status_code=status.HTTP_201_CREATED)

async def add_module(

    module_in: CourseModuleCreate,

    db: AsyncSession = Depends(get_db),

    school_id=Depends(get_current_school_id),

    _=Depends(RequirePermissions([Permission.MANAGE_COURSES]))

):

    module = await create_module(db, module_in, school_id)

    if not module:

        raise HTTPException(status_code=404, detail="Kurs topilmadi yoki bu maktabga tegishli emas")

    return module

@router.get("/course/{course_id}", response_model=List[LessonResponse])

async def list_lessons(course_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Kursga tegishli barcha darslar ro'yxati (tartib bo'yicha)."""

    return await get_lessons_by_course(db, course_id, school_id)

@router.get("/{lesson_id}", response_model=LessonResponse)

async def get_lesson(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db), school_id=Depends(get_current_school_id)):

    """Bitta darsni olish."""

    lesson = await get_lesson_by_id(db, lesson_id, school_id)

    if not lesson:

        raise HTTPException(status_code=404, detail="Dars topilmadi")

    return lesson

@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)

async def add_lesson(

    lesson_in: LessonCreate,

    db: AsyncSession = Depends(get_db),

    school_id=Depends(get_current_school_id),

    _=Depends(RequirePermissions([Permission.MANAGE_COURSES]))

):

    """Yangi dars qo'shish (faqat admin/manager/o'qituvchi)."""

    lesson = await create_lesson(db, lesson_in, school_id)

    if not lesson:

        raise HTTPException(status_code=404, detail="Kurs topilmadi yoki bu maktabga tegishli emas")

    return lesson

@router.put("/{lesson_id}", response_model=LessonResponse)

async def edit_lesson(

    lesson_id: uuid.UUID,

    lesson_in: LessonCreate,

    db: AsyncSession = Depends(get_db),

    school_id=Depends(get_current_school_id),

    _=Depends(RequirePermissions([Permission.MANAGE_COURSES]))

):

    """Darsni tahrirlash."""

    lesson = await update_lesson(db, lesson_id, lesson_in, school_id)

    if not lesson:

        raise HTTPException(status_code=404, detail="Dars topilmadi")

    return lesson

@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)

async def remove_lesson(

    lesson_id: uuid.UUID,

    db: AsyncSession = Depends(get_db),

    school_id=Depends(get_current_school_id),

    _=Depends(RequirePermissions([Permission.MANAGE_COURSES]))

):

    """Darsni o'chirish."""

    lesson = await delete_lesson(db, lesson_id, school_id)

    if not lesson:

        raise HTTPException(status_code=404, detail="Dars topilmadi")

