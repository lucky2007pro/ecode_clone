from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_payments():
    return [{"provider": "payme", "status": "paid"}]
