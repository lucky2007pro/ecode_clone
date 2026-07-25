"""
Gmail Free SMTP Transactional Email & Email OTP Verification Service.
"""
import os
import random
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("email_service")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "usa20070302@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS", "zgrj syhw cuby dopg")


async def send_smtp_email(to_email: str, subject: str, body_html: str) -> bool:
    """Gmail SMTP orqali HTML email jo'natadi."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Exode.biz Platformasi <{SMTP_USER}>"
        msg["To"] = to_email

        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        logger.info(f"Gmail email muvaffaqiyatli jo'natildi -> To: {to_email}")
        return True
    except Exception as e:
        logger.error(f"Gmail email jo'natishda xatolik: {e}")
        return False


async def send_email_otp(to_email: str) -> str:
    """6 xonali bepul Email OTP kod generatsiya qiladi va Gmail orqali yuboradi."""
    otp_code = str(random.randint(100000, 999999))

    subject = f"Exode.biz — Tasdiqlash kodingiz: {otp_code}"
    body = f"""
    <div style="font-family: Arial, sans-serif; padding: 25px; background: #0f172a; color: #fff; border-radius: 16px; max-width: 500px; margin: 0 auto;">
        <h2 style="color: #6366f1; margin-top: 0;">Exode.biz Platformasi</h2>
        <p style="color: #cbd5e1; font-size: 15px;">Ro'yxatdan o'tishni tasdiqlash uchun kodingiz:</p>
        <div style="font-size: 34px; font-weight: 800; color: #10b981; letter-spacing: 6px; margin: 24px 0; background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; text-align: center;">
            {otp_code}
        </div>
        <p style="font-size: 13px; color: #94a3b8;">Ushbu kod 5 daqiqa davomida amal qiladi. Kodni hech kimga bermang.</p>
        <hr style="border-color: rgba(255,255,255,0.1); margin-top: 20px;" />
        <p style="font-size: 11px; color: #64748b; text-align: center;">Exode.biz — Onlayn Maktab va Kurslar Platformasi</p>
    </div>
    """
    await send_smtp_email(to_email, subject, body)
    return otp_code
