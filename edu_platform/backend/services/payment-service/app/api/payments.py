"""
Payments API Router.
"""
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import Payment, Subscription
from app.schemas import PaymentCreate, PaymentResponse, SubscriptionCreate, SubscriptionResponse
from libs.shared_schemas.enums import PaymentStatus

router = APIRouter()


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(pay_in: PaymentCreate, db: AsyncSession = Depends(get_db)):
    """Yangi to'lov so'rovi yaratadi (Payme/Click)."""
    payment = Payment(
        user_id=pay_in.user_id,
        school_id=pay_in.school_id,
        course_id=pay_in.course_id,
        amount=pay_in.amount,
        provider=pay_in.provider,
        status=PaymentStatus.pending,
    )
    db.add(payment)
    await db.flush()
    return payment


@router.get("/user/{user_id}", response_model=list[PaymentResponse])
async def get_user_payments(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Foydalanuvchining barcha to'lovlar tarixi."""
    stmt = select(Payment).where(Payment.user_id == user_id)
    res = await db.execute(stmt)
    return list(res.scalars().all())
