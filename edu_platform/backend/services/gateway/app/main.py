"""
API Gateway — barcha so'rovlarni tegishli servisga yo'naltiradi.
JWT tokenni tekshiradi, rate-limit va WebSocket Chat'ni boshqaradi.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router
from app.websocket_chat import router as chat_ws_router

app = FastAPI(
    title="Exode Platform — API Gateway",
    description="Barcha mikroservislarni va WebSocket Chat'ni birlashtiradigan gateway",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(chat_ws_router, tags=["chat_ws"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "gateway"}
