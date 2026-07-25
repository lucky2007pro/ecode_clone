"""
Tariffs API Router.
"""
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import TariffPlanCreate, TariffPlanResponse
from app.services.school_service import create_tariff_plan, get_tariff_plans, get_tariff_plan_by_id

router = APIRouter()


@router.post("/", response_model=TariffPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_tariff(tariff_in: TariffPlanCreate, db: AsyncSession = Depends(get_db)):
    """Yangi tarif rejasini yaratadi (Adminlar uchun)."""
    return await create_tariff_plan(db, tariff_in)


@router.get("/", response_model=list[TariffPlanResponse])
async def list_tariffs(db: AsyncSession = Depends(get_db)):
    """Barcha tarif rejalari ro'yxati."""
    return await get_tariff_plans(db)


@router.get("/{tariff_id}", response_model=TariffPlanResponse)
async def get_tariff(tariff_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Bitta tarif rejasini ko'rish."""
    return await get_tariff_plan_by_id(db, tariff_id)
