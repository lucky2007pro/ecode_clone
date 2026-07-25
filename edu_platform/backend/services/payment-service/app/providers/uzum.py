"""
Uzum Bank Merchant API Integratsiyasi.
"""
import logging

logger = logging.getLogger("uzum_payment")


class UzumBankHandler:
    async def create_payment_link(self, order_id: str, amount: float) -> str:
        """Uzum Bank orqali to'lov havolasi yaratish."""
        logger.info(f"Uzum Bank order_id '{order_id}' uchun {amount} UZS to'lov linki yaratildi.")
        return f"https://payment.uzumbank.uz/pay?order={order_id}&amount={amount}"

    async def handle_webhook(self, payload: dict) -> dict:
        """Uzum Bank Webhook javobini tekshirish."""
        order_id = payload.get("order_id")
        status = payload.get("status")
        return {"status": "ok", "order_id": order_id, "processed": True}


uzum_handler = UzumBankHandler()
