"""
Payme Merchant JSON-RPC 2.0 Protocol ishlovchisi.
"""
import uuid
from typing import Any


class PaymeMerchantHandler:
    def __init__(self):
        pass

    async def handle_request(self, payload: dict) -> dict:
        method = payload.get("method")
        params = payload.get("params", {})
        request_id = payload.get("id")

        if method == "CheckPerformTransaction":
            return self._success_response(request_id, {"allow": True})
        elif method == "CreateTransaction":
            return self._success_response(
                request_id,
                {
                    "create_time": 1600000000000,
                    "transaction": str(params.get("id")),
                    "state": 1,
                },
            )
        elif method == "PerformTransaction":
            return self._success_response(
                request_id,
                {
                    "transaction": str(params.get("id")),
                    "perform_time": 1600000000000,
                    "state": 2,
                },
            )
        elif method == "CancelTransaction":
            return self._success_response(
                request_id,
                {
                    "transaction": str(params.get("id")),
                    "cancel_time": 1600000000000,
                    "state": -1,
                },
            )
        elif method == "CheckTransaction":
            return self._success_response(
                request_id,
                {
                    "create_time": 1600000000000,
                    "perform_time": 1600000000000,
                    "cancel_time": 0,
                    "transaction": str(params.get("id")),
                    "state": 2,
                    "reason": None,
                },
            )
        else:
            return {
                "error": {"code": -32601, "message": "Method not found"},
                "id": request_id,
            }

    def _success_response(self, request_id: Any, result: dict) -> dict:
        return {"result": result, "error": None, "id": request_id}


payme_handler = PaymeMerchantHandler()
