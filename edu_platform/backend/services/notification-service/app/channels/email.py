"""
SMTP Transaksion Email jo'natish xizmati.
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("email_channel")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "noreply@exode.biz"
SMTP_PASS = "your-smtp-password"


async def send_email(to_email: str, subject: str, body: str) -> bool:
    """SMTP orqali HTML transactional email jo'natadi."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email

        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #0f172a; color: #f8fafc; border-radius: 12px;">
            <h2 style="color: #818cf8;">Exode Platformasi</h2>
            <p>{body}</p>
            <hr style="border-color: rgba(255,255,255,0.1);" />
            <p style="font-size: 12px; color: #94a3b8;">Exode.biz — Onlayn Maktab va Kurslar Platformasi</p>
        </div>
        """
        msg.attach(MIMEText(html_content, "html"))

        # Non-blocking async handling
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        logger.info(f"Email muvaffaqiyatli jo'natildi -> To: {to_email}")
        return True
    except Exception as e:
        logger.error(f"Email jo'natishda xatolik: {e}")
        return False
