from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from messages.models import Message
import uuid

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str, sender: str = "System"):
        for connection in self.active_connections:
            await connection.send_json({"sender": sender, "text": message})


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # MVP: barchaga tarqatish
            await manager.broadcast(data, sender="User")
            
            # DB ga saqlash uchun logikani yozish mumkin (global chat sifatida mock qilamiz)
            # Lekin WebSocket sessiyasi ichida db.commit qilish biroz xavfli bo'lishi mumkin 
            # chunki AsyncSession bitta ish zarrachasiga (thread) bog'langan bo'ladi.
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Foydalanuvchi chatdan chiqdi", sender="System")


@router.get("/history")
async def get_chat_history(db: AsyncSession = Depends(get_db)):
    """Global chat tarixini olish."""
    res = await db.execute(select(Message).order_by(Message.created_at.desc()).limit(50))
    messages = res.scalars().all()
    # Teskari tartibda qaytaramizki xronologik to'g'ri bo'lsin
    return [{"id": m.id, "content": m.content, "sender_id": m.sender_id, "created_at": m.created_at} for m in messages[::-1]]
