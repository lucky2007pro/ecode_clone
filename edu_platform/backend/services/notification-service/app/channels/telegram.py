"""
Telegram Bot integratsiya xizmati (httpx orqali Telegram Bot API).
Yopiq kanal/guruhga taklif havolasi (Invite Link) generatsiya qilish va xabarlar jo'natish.
"""
import logging
import httpx

logger = logging.getLogger("telegram_channel")

BOT_TOKEN = "your-telegram-bot-token-here"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def send_telegram_message(chat_id: str | int, text: str) -> bool:
    """Telegram foydalanuvchisi yoki guruhiga xabar jo'natadi."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            res = await client.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            )
            return res.status_code == 200
        except Exception as e:
            logger.error(f"Telegram sendMessage xatolik: {e}")
            return False


async def create_telegram_invite_link(channel_id: str | int) -> str | None:
    """
    To'lov qilgan o'quvchi uchun Telegram yopiq kanaliga 1 marta ishlatiladigan
    taklif havolasi (Single-use Invite Link) yaratadi.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            res = await client.post(
                f"{TELEGRAM_API_URL}/createChatInviteLink",
                json={
                    "chat_id": channel_id,
                    "member_limit": 1,  # Faqat 1 kishi kirishi mumkin
                    "name": "To'lovdan keyingi taklif havolasi",
                },
            )
            if res.status_code == 200:
                data = res.json()
                return data.get("result", {}).get("invite_link")
            return None
        except Exception as e:
            logger.error(f"Telegram createChatInviteLink xatolik: {e}")
            return None
