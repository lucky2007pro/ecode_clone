from datetime import datetime, timezone, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from payments.models import SchoolSubscription, Transaction, TransactionType, SubscriptionStatus
from payments.schema import PlanResponse, SubscribeRequest, SchoolSubscriptionResponse, TopUpRequest, TransactionResponse
from notifications.crud import create_notification
from permissions.dependencies import get_current_user, get_current_school_id
from permissions.enums import Role
from users.models import User
from schools.models import UserSchool

router = APIRouter()

# Platforma tariflari (MVP — kod ichida konstanta)
PLANS = [
    PlanResponse(id="starter", name="Boshlang'ich", price=100_000, months=1,
                 features=["50 o'quvchi", "3 kurs"]),
    PlanResponse(id="standard", name="Standart", price=300_000, months=1,
                 features=["200 o'quvchi", "10 kurs", "Tavsiya etiladi"]),
    PlanResponse(id="premium", name="Premium", price=600_000, months=1,
                 features=["Cheksiz o'quvchi", "Cheksiz kurslar"]),
]


def _role_of(user) -> Role:
    return user.role if isinstance(user.role, Role) else Role(user.role)


def _require_roles(*roles: Role):
    async def checker(user=Depends(get_current_user)):
        if _role_of(user) not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ruxsat yo'q")
        return user
    return checker


@router.get("/plans", response_model=List[PlanResponse])
async def list_plans():
    return PLANS


@router.post("/subscribe", response_model=SchoolSubscriptionResponse)
async def subscribe(req: SubscribeRequest, db: AsyncSession = Depends(get_db),
                    school_id=Depends(get_current_school_id),
                    user=Depends(_require_roles(Role.ADMIN))):
    plan = next((p for p in PLANS if p.id == req.plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Tarif topilmadi")
    if float(user.balance) < plan.price:
        raise HTTPException(status_code=400, detail="Balans yetarli emas")

    user.balance = float(user.balance) - plan.price

    # Eski faol obunani bekor qilamiz
    res = await db.execute(
        select(SchoolSubscription).where(
            SchoolSubscription.school_id == school_id,
            SchoolSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    old = res.scalars().first()
    if old:
        old.status = SubscriptionStatus.CANCELED

    expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30)
    subscription = SchoolSubscription(school_id=school_id, plan_name=plan.name, expires_at=expires_at)
    db.add(subscription)
    db.add(Transaction(user_id=user.id, school_id=school_id, amount=plan.price,
                       type=TransactionType.OUT, description=f"Platforma obunasi: {plan.name}"))
    await db.commit()
    await db.refresh(subscription)
    return SchoolSubscriptionResponse(plan_name=subscription.plan_name,
                                      status=subscription.status.value,
                                      expires_at=subscription.expires_at)


@router.get("/school-subscription", response_model=SchoolSubscriptionResponse | None)
async def get_school_subscription(db: AsyncSession = Depends(get_db),
                                  school_id=Depends(get_current_school_id),
                                  _=Depends(get_current_user)):
    res = await db.execute(
        select(SchoolSubscription)
        .where(SchoolSubscription.school_id == school_id,
               SchoolSubscription.status == SubscriptionStatus.ACTIVE)
        .order_by(SchoolSubscription.created_at.desc())
    )
    sub = res.scalars().first()
    if not sub:
        return None
    return SchoolSubscriptionResponse(plan_name=sub.plan_name, status=sub.status.value, expires_at=sub.expires_at)


@router.post("/topup", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def topup(req: TopUpRequest, db: AsyncSession = Depends(get_db),
                school_id=Depends(get_current_school_id),
                _=Depends(_require_roles(Role.ADMIN, Role.MANAGER, Role.ACCOUNTANT))):
    res = await db.execute(select(User).where(User.id == req.user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    user.balance = float(user.balance) + req.amount
    description = req.description or "Balans to'ldirish"
    tx = Transaction(user_id=user.id, school_id=school_id, amount=req.amount,
                     type=TransactionType.IN, description=description)
    db.add(tx)
    await db.commit()
    await db.refresh(tx)

    await create_notification(db, user.id, school_id,
                              "Balans to'ldirildi",
                              f"Hisobingiz to'ldirildi: {req.amount:,.0f} UZS")
    return TransactionResponse(id=tx.id, amount=float(tx.amount), type=tx.type.value,
                               description=tx.description, created_at=tx.created_at)


@router.get("/transactions/me", response_model=List[TransactionResponse])
async def my_transactions(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user.id)
        .order_by(Transaction.created_at.desc())
        .limit(50)
    )
    return [
        TransactionResponse(id=t.id, amount=float(t.amount), type=t.type.value if hasattr(t.type, 'value') else t.type,
                            description=t.description or "", created_at=t.created_at)
        for t in res.scalars().all()
    ]


@router.get("/transactions", response_model=List[TransactionResponse])
async def all_school_transactions(db: AsyncSession = Depends(get_db),
                                  school_id=Depends(get_current_school_id),
                                  _=Depends(_require_roles(Role.ADMIN, Role.MANAGER, Role.ACCOUNTANT))):
    user_ids_res = await db.execute(select(UserSchool.user_id).where(UserSchool.school_id == school_id))
    user_ids = user_ids_res.scalars().all()

    res = await db.execute(
        select(Transaction)
        .where((Transaction.school_id == school_id) | (Transaction.user_id.in_(user_ids) if user_ids else False))
        .order_by(Transaction.created_at.desc())
        .limit(100)
    )
    return [
        TransactionResponse(
            id=t.id, 
            amount=float(t.amount), 
            type=t.type.value if hasattr(t.type, 'value') else t.type,
            description=t.description or "", 
            created_at=t.created_at
        )
        for t in res.scalars().all()
    ]
