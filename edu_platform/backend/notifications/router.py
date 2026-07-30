import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, EmailStr

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

from notifications.email import send_email_otp, send_smtp_email_task

from notifications.telegram import send_telegram_msg

from notifications.schema import NotificationListResponse, NotificationResponse

from notifications.crud import (

    get_user_notifications, count_unread, mark_notification_read, mark_all_notifications_read,

)

from permissions.dependencies import get_current_user

router = APIRouter()

class EmailOTPRequest(BaseModel):

    email: EmailStr

class EmailOTPVerify(BaseModel):

    email: EmailStr

    code: str

@router.post("/send-otp", status_code=status.HTTP_200_OK)

async def send_otp(req: EmailOTPRequest):

    """Gmail orqali 6 xonali bepul OTP tasdiqlash kodini yuboradi."""

    otp = await send_email_otp(req.email)

    return {"status": "success", "message": f"OTP kod {req.email} ga yuborildi"}

@router.post("/send-email", status_code=status.HTTP_200_OK)

async def send_custom_email(email: EmailStr, subject: str, message: str):

    """Gmail orqali xabar jo'natish."""

    send_smtp_email_task.delay(email, subject, f"<p>{message}</p>")

    return {"status": "sent"}

@router.get("/", response_model=NotificationListResponse)

async def list_my_notifications(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):

    """Joriy foydalanuvchining bildirishnomalari (yangisi birinchi)."""

    results = await get_user_notifications(db, current_user.id)

    unread = await count_unread(db, current_user.id)

    return {"unread_count": unread, "results": results}

@router.post("/read-all", status_code=status.HTTP_204_NO_CONTENT)

async def read_all_notifications(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):

    """Barcha bildirishnomalarni o'qilgan deb belgilash."""

    await mark_all_notifications_read(db, current_user.id)

@router.post("/{notification_id}/read", response_model=NotificationResponse)

async def read_one_notification(notification_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):

    """Bitta bildirishnomani o'qilgan deb belgilash."""

    notification = await mark_notification_read(db, notification_id, current_user.id)

    if not notification:

        raise HTTPException(status_code=404, detail="Bildirishnoma topilmadi")

    return notification

