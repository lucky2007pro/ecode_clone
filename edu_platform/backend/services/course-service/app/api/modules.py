"""
Modules API Router.
"""
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import ModuleCreate, ModuleResponse
from app.services.course_service import create_module, get_modules_by_course

router = APIRouter()


@router.post("/", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_new_module(module_in: ModuleCreate, db: AsyncSession = Depends(get_db)):
    """Kurs ichida yangi modul yaratish."""
    return await create_module(db, module_in)


@router.get("/course/{course_id}", response_model=list[ModuleResponse])
async def list_modules(course_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Kursning modullar ro'yxatini olish."""
    return await get_modules_by_course(db, course_id)
