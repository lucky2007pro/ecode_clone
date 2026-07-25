"""
Payme va Click webhook router'lari.
"""
from fastapi import APIRouter, Request, status
from app.providers.payme import payme_handler
from app.providers.click import click_handler

router = APIRouter()


@router.post("/payme", status_code=status.HTTP_200_OK)
async def handle_payme_webhook(request: Request):
    """Payme JSON-RPC webhooklarini qabul qiladi."""
    payload = await request.json()
    return await payme_handler.handle_request(payload)


@router.post("/click/prepare", status_code=status.HTTP_200_OK)
async def handle_click_prepare(request: Request):
    """Click Prepare webhook."""
    form_data = await request.form()
    return await click_handler.prepare(dict(form_data))


@router.post("/click/complete", status_code=status.HTTP_200_OK)
async def handle_click_complete(request: Request):
    """Click Complete webhook."""
    form_data = await request.form()
    return await click_handler.complete(dict(form_data))
