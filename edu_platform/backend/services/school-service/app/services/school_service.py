"""
school-service biznes mantiqiy servisi (TariffPlan va School CRUD).
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models import School, TariffPlan
from app.schemas import SchoolCreate, SchoolUpdate, TariffPlanCreate


# --- TARIFF PLAN SERVICES ---
async def create_tariff_plan(db: AsyncSession, tariff_in: TariffPlanCreate) -> TariffPlan:
    tariff = TariffPlan(**tariff_in.model_dump())
    db.add(tariff)
    await db.flush()
    return tariff


async def get_tariff_plans(db: AsyncSession) -> list[TariffPlan]:
    stmt = select(TariffPlan)
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def get_tariff_plan_by_id(db: AsyncSession, tariff_id: uuid.UUID) -> TariffPlan:
    tariff = await db.get(TariffPlan, tariff_id)
    if not tariff:
        raise HTTPException(status_code=404, detail="Tarif rejasi topilmadi")
    return tariff


# --- SCHOOL SERVICES ---
async def create_school(db: AsyncSession, school_in: SchoolCreate) -> School:
    # Subdomen takrorlanmasligini tekshirish
    stmt = select(School).where(School.subdomain == school_in.subdomain)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday subdomen allaqachon band qilingan",
        )

    # Tarif plani borligini tekshirish
    await get_tariff_plan_by_id(db, school_in.tariff_plan_id)

    school = School(**school_in.model_dump())
    db.add(school)
    await db.flush()
    return school


async def get_schools(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[School]:
    stmt = select(School).offset(skip).limit(limit)
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def get_school_by_id(db: AsyncSession, school_id: uuid.UUID) -> School:
    school = await db.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="Maktab topilmadi")
    return school


async def get_school_by_subdomain(db: AsyncSession, subdomain: str) -> School:
    stmt = select(School).where(School.subdomain == subdomain)
    res = await db.execute(stmt)
    school = res.scalar_one_or_none()
    if not school:
        raise HTTPException(status_code=404, detail="Maktab subdomeni topilmadi")
    return school


async def update_school(db: AsyncSession, school_id: uuid.UUID, school_update: SchoolUpdate) -> School:
    school = await get_school_by_id(db, school_id)
    update_data = school_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(school, field, value)

    await db.flush()
    return school
