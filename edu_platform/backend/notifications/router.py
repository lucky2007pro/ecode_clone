from fastapi import APIRouter
router = APIRouter()

@router.post("/send")
async def send_notification(user_id: str, message: str):
    return {"status": "sent"}
