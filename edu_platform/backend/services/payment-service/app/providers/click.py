"""
Click Merchant Protocol ishlovchisi (Prepare & Complete).
"""


class ClickMerchantHandler:
    async def prepare(self, params: dict) -> dict:
        click_trans_id = params.get("click_trans_id")
        merchant_trans_id = params.get("merchant_trans_id")
        amount = params.get("amount")

        return {
            "error": 0,
            "error_note": "Success",
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "merchant_prepare_id": 1,
        }

    async def complete(self, params: dict) -> dict:
        click_trans_id = params.get("click_trans_id")
        merchant_trans_id = params.get("merchant_trans_id")

        return {
            "error": 0,
            "error_note": "Success",
            "click_trans_id": click_trans_id,
            "merchant_trans_id": merchant_trans_id,
            "merchant_confirm_id": 1,
        }


click_handler = ClickMerchantHandler()
