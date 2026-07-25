from fastapi import APIRouter
from crm.kommo import send_lead_to_kommo

router = APIRouter()

@router.post("/lead")
async def create_lead(name: str, phone: str):
    return await send_lead_to_kommo(name, phone)
