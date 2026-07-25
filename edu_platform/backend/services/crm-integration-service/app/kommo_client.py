"""
Kommo (amoCRM) API v4 asinxron client wrapper.
"""
import httpx
from fastapi import HTTPException
from app.core.config import settings


class KommoClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.KOMMO_LONG_LIVED_TOKEN}",
            "Content-Type": "application/json",
        }

    async def create_lead_complex(self, full_name: str, email: str, phone: str | None = None) -> dict:
        """
        POST /api/v4/leads/complex
        Lid (Bitim) va Kontaktni bitta API so'rovida yaratadi.
        """
        payload = [
            {
                "name": f"Lid: {full_name}",
                "price": 0,
                "_embedded": {
                    "contacts": [
                        {
                            "name": full_name,
                            "custom_fields_values": [
                                {
                                    "field_code": "EMAIL",
                                    "values": [{"value": email, "enum_code": "WORK"}],
                                },
                                *(
                                    [
                                        {
                                            "field_code": "PHONE",
                                            "values": [{"value": phone, "enum_code": "WORK"}],
                                        }
                                    ]
                                    if phone
                                    else []
                                ),
                            ],
                        }
                    ]
                },
            }
        ]

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.KOMMO_API_URL}/leads/complex",
                headers=self.headers,
                json=payload,
            )
            if response.status_code not in (200, 201):
                raise HTTPException(
                    status_code=500,
                    detail=f"Kommo API bilan xatolik: {response.text}",
                )

            res_data = response.json()
            if isinstance(res_data, list) and len(res_data) > 0:
                lead_info = res_data[0]
                return {
                    "kommo_lead_id": str(lead_info.get("id")),
                    "kommo_contact_id": str(lead_info.get("contact_id")) if lead_info.get("contact_id") else None,
                }
            return {}

    async def update_lead_status(self, kommo_lead_id: str, status_id: int) -> bool:
        """
        PATCH /api/v4/leads/{id}
        Lid statusini (masalan 'To'landi') o'zgartirish.
        """
        payload = [{"id": int(kommo_lead_id), "status_id": status_id}]

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.patch(
                f"{settings.KOMMO_API_URL}/leads",
                headers=self.headers,
                json=payload,
            )
            return response.status_code in (200, 201)


kommo_client = KommoClient()
