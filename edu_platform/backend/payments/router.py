from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from db import get_db
from payments.models import PaymentPlan, Subscription, PlanType, SubscriptionStatus, Transaction, TransactionType, SchoolSubscription
from users.models import User
from permissions.dependencies import RequirePermissions, get_current_school_id
from permissions.enums import Permission

router = APIRouter()

class PaymentPlanCreate(BaseModel):
    course_id: uuid.UUID
    name: str
    plan_type: PlanType
    price: float
    months: int = 1

@router.post("/plans")
async def create_payment_plan(plan_in: PaymentPlanCreate, db: AsyncSession = Depends(get_db), _=Depends(RequirePermissions([Permission.MANAGE_PRODUCTS]))):
    new_plan = PaymentPlan(**plan_in.dict())
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan

@router.get("/plans/{course_id}")
async def get_course_plans(course_id: uuid.UUID, db: AsyncSession = Depends(get_db), _=Depends(RequirePermissions([Permission.VIEW_FINANCE]))):
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

class SchoolSubscribeRequest(BaseModel):
    user_id: uuid.UUID
    school_id: uuid.UUID
    plan_name: str
    price: float

@router.post("/school-subscribe")
async def subscribe_school(req: SchoolSubscribeRequest, db: AsyncSession = Depends(get_db), _=Depends(RequirePermissions([Permission.MANAGE_PRODUCTS]))):
    user_res = await db.execute(select(User).where(User.id == req.user_id))
    user = user_res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.balance < req.price:
        raise HTTPException(status_code=400, detail="Balansda yetarli mablag' mavjud emas")
        
    # Deduct balance
    user.balance -= req.price
    db.add(user)
    
    # Create transaction
    transaction = Transaction(
        user_id=user.id,
        school_id=req.school_id,
        amount=req.price,
        type=TransactionType.OUT,
        description=f"Platforma obunasi: {req.plan_name}"
    )
    db.add(transaction)
    
    # Create school subscription
    expires_at = datetime.utcnow() + timedelta(days=30)
    school_sub = SchoolSubscription(
        school_id=req.school_id,
        plan_name=req.plan_name,
        expires_at=expires_at,
        status=SubscriptionStatus.ACTIVE
    )
    db.add(school_sub)
    
    await db.commit()
    return {"status": "success", "message": "Obuna muvaffaqiyatli xarid qilindi"}

class TransactionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    school_id: Optional[uuid.UUID]
    amount: float
    type: str
    description: str
    created_at: datetime
    
    class Config:
        orm_mode = True

@router.get("/transactions/{school_id}", response_model=List[TransactionResponse])
async def get_transactions(school_id: uuid.UUID, db: AsyncSession = Depends(get_db), token_school_id=Depends(get_current_school_id), _=Depends(RequirePermissions([Permission.VIEW_FINANCE]))):
    if school_id != token_school_id:
        raise HTTPException(status_code=403, detail="Boshqa maktab ma'lumotiga kirish taqiqlangan")
    # We return all transactions for the users in this school?
    # Or transactions associated with this school.
    # We should return transactions where transaction.school_id == school_id 
    # OR transactions made by users who belong to this school. 
    # For now, let's just return all transactions (since it's a demo, we can just return all or fetch by school_id).
    # Since we didn't link all transactions to school_id initially in enrollments, we can fetch all for now,
    # or let's just fetch all transactions. The frontend will display them.
    res = await db.execute(select(Transaction).where(Transaction.school_id == token_school_id).order_by(Transaction.created_at.desc()))
    transactions = res.scalars().all()
    
    result = []
    for t in transactions:
        result.append(TransactionResponse(
            id=t.id,
            user_id=t.user_id,
            school_id=t.school_id,
            amount=t.amount,
            type=t.type.value,
            description=t.description,
            created_at=t.created_at
        ))
    return result
