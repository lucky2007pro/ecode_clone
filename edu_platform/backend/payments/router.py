from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from db import get_db
from payments.models import PaymentPlan, Subscription, PlanType, SubscriptionStatus

router = APIRouter()

class PaymentPlanCreate(BaseModel):
    course_id: uuid.UUID
    name: str
    plan_type: PlanType
    price: float
    months: int = 1

@router.post("/plans")
async def create_payment_plan(plan_in: PaymentPlanCreate, db: AsyncSession = Depends(get_db)):
    new_plan = PaymentPlan(**plan_in.dict())
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan

@router.get("/plans/{course_id}")
async def get_course_plans(course_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(PaymentPlan).where(PaymentPlan.course_id == course_id))
    return res.scalars().all()

class SubscribeRequest(BaseModel):
    user_id: uuid.UUID
    plan_id: uuid.UUID

@router.post("/subscribe")
async def subscribe_to_plan(req: SubscribeRequest, db: AsyncSession = Depends(get_db)):
    # Calculate next payment date
    next_date = datetime.utcnow() + timedelta(days=30)
    
    sub = Subscription(
        user_id=req.user_id,
        plan_id=req.plan_id,
        status=SubscriptionStatus.ACTIVE,
        next_payment_date=next_date
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub

@router.get("/subscriptions/{user_id}")
async def get_user_subscriptions(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    return res.scalars().all()
