"""
Marketing & Conversion Tracker (Facebook Pixel API & Google Analytics 4 Measurement Protocol).
UTM parametrlari va reklama konversiyalarini kuzatish.
"""
import logging
import httpx

logger = logging.getLogger("marketing_tracker")

FB_PIXEL_ID = "your-facebook-pixel-id"
FB_ACCESS_TOKEN = "your-facebook-conversions-token"
GA4_MEASUREMENT_ID = "G-XXXXXXXXXX"
GA4_API_SECRET = "your-ga4-api-secret"


async def track_facebook_conversion(event_name: str, user_email: str, amount: float = 0.0) -> bool:
    """Facebook Conversions API orqali hodisani (Purchase / Lead) yuboradi."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"https://graph.facebook.com/v18.0/{FB_PIXEL_ID}/events?access_token={FB_ACCESS_TOKEN}"
            payload = {
                "data": [
                    {
                        "event_name": event_name,
                        "event_time": 1600000000,
                        "user_data": {"em": [user_email]},
                        "custom_data": {"currency": "UZS", "value": amount},
                    }
                ]
            }
            res = await client.post(url, json=payload)
            return res.status_code == 200
        except Exception as e:
            logger.error(f"Facebook conversion tracker xatolik: {e}")
            return False


async def track_ga4_event(client_id: str, event_name: str, params: dict | None = None) -> bool:
    """Google Analytics 4 Measurement Protocol orqali hodisa yuborish."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"https://www.google-analytics.com/mp/collect?measurement_id={GA4_MEASUREMENT_ID}&api_secret={GA4_API_SECRET}"
            payload = {
                "client_id": client_id,
                "events": [{"name": event_name, "params": params or {}}],
            }
            res = await client.post(url, json=payload)
            return res.status_code in (200, 204)
        except Exception as e:
            logger.error(f"GA4 tracker xatolik: {e}")
            return False
