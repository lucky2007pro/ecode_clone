"""
Schools API Router.
"""
import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import SchoolCreate, SchoolUpdate, SchoolResponse
from app.services.school_service import (
    create_school,
    get_schools,
    get_school_by_id,
    get_school_by_subdomain,
    update_school,
)

router = APIRouter()


@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def create_new_school(school_in: SchoolCreate, db: AsyncSession = Depends(get_db)):
    """Yangi maktab ro'yxatga oladi (Tenant)."""
    return await create_school(db, school_in)


@router.get("/", response_model=list[SchoolResponse])
async def list_schools(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Maktablar ro'yxati."""
    return await get_schools(db, skip=skip, limit=limit)


@router.get("/subdomain/{subdomain}", response_model=SchoolResponse)
async def get_by_subdomain(subdomain: str, db: AsyncSession = Depends(get_db)):
    """Subdomen bo'yicha maktab sozlamalarini olish."""
    return await get_school_by_subdomain(db, subdomain)


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(school_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Maktabni ID bo'yicha olish."""
    return await get_school_by_id(db, school_id)


@router.patch("/{school_id}", response_model=SchoolResponse)
async def patch_school(
    school_id: uuid.UUID,
    school_update: SchoolUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Maktab sozlamalari yoki tarifini yangilash."""
    return await update_school(db, school_id, school_update)
