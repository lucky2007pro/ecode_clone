"""
Eskiz.uz SMS Gateway API integratsiyasi.
OAuth 2.0 Token olish va SMS jo'natish.
"""
import logging
import httpx

logger = logging.getLogger("eskiz_sms")

ESKIZ_EMAIL = "your-eskiz-email@exode.biz"
ESKIZ_PASSWORD = "your-eskiz-password"
ESKIZ_API_URL = "https://notify.eskiz.uz/api"


class EskizSMSClient:
    def __init__(self):
        self.token: str | None = None

    async def _get_token(self) -> str | None:
        """Eskiz API token olish."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                res = await client.post(
                    f"{ESKIZ_API_URL}/auth/login",
                    data={"email": ESKIZ_EMAIL, "password": ESKIZ_PASSWORD},
                )
                if res.status_code == 200:
                    data = res.json()
                    self.token = data.get("data", {}).get("token")
                    return self.token
                return None
            except Exception as e:
                logger.error(f"Eskiz auth login xatolik: {e}")
                return None

    async def send_sms(self, phone: str, message: str) -> bool:
        """Telefon raqamga SMS jo'natish."""
        if not self.token:
            await self._get_token()

        # Telefon raqamni formatlash (998901234567)
        clean_phone = phone.replace("+", "").replace(" ", "")

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                res = await client.post(
                    f"{ESKIZ_API_URL}/message/sms/send",
                    headers={"Authorization": f"Bearer {self.token}"},
                    data={
                        "mobile_phone": clean_phone,
                        "message": message,
                        "from": "4546",  # Eskiz qisqa raqam kodi
                    },
                )
                if res.status_code == 401:  # Token muddati o'tgan bo'lsa qayta olamiz
                    await self._get_token()
                    return await self.send_sms(phone, message)

                return res.status_code == 200
            except Exception as e:
                logger.error(f"Eskiz send_sms xatolik: {e}")
                return False


eskiz_client = EskizSMSClient()


async def send_sms(phone: str, message: str) -> bool:
    """Umumiy SMS yuborish chaqirig'i."""
    return await eskiz_client.send_sms(phone, message)
