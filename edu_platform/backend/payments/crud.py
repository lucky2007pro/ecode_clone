from sqlalchemy.ext.asyncio import AsyncSession
from payments.models import Payment
from payments.schema import PaymentCreate

async def create_payment(db: AsyncSession, pay_in: PaymentCreate):
    p = Payment(**pay_in.model_dump())
    db.add(p)
    await db.flush()
    return p
