"""
Gmail Email OTP va Telegram Notifications Router.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from notifications.email import send_email_otp, send_smtp_email_task
from notifications.telegram import send_telegram_msg

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
