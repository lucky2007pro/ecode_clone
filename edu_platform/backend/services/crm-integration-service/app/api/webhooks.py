"""
Kommo Webhook router.
Kommo'da menejer deal statusini o'zgartirganda so'rov qabul qiladi.
"""
from fastapi import APIRouter, status, Request

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def handle_kommo_webhook(request: Request):
    """
    Kommo webhooklarini 5 sekund ichida 200 OK qaytarib qabul qiladi.
    """
    try:
        body = await request.form()
        # Kommo form-urlencoded formatda yuboradi
        data = dict(body)
        # Audit va asinxron qayta ishlash uchun
        return {"status": "ok", "received": True}
    except Exception:
        return {"status": "ok", "received": True}
