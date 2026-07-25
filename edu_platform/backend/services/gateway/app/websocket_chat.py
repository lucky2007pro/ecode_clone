"""
FastAPI WebSocket Messendjer Router (Platforma ichidagi Real-time Chat).
O'quvchi va Kuratorlar o'rtasida muloqot va fayl ulashish.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging

logger = logging.getLogger("websocket_chat")

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        # room_id -> list of WebSockets
        self.active_rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = []
        self.active_rooms[room_id].append(websocket)
        logger.info(f"Yangi mijoz xonaga ulandi: room_id='{room_id}'")

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_rooms:
            self.active_rooms[room_id].remove(websocket)
            if not self.active_rooms[room_id]:
                del self.active_rooms[room_id]

    async def broadcast_to_room(self, room_id: str, message: dict):
        if room_id in self.active_rooms:
            for connection in self.active_rooms[room_id]:
                await connection.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/chat/{room_id}")
async def websocket_chat_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data_str = await websocket.receive_text()
            try:
                data = json.loads(data_str)
                # Chat message payload: { "sender_name": "...", "text": "...", "file_url": "..." }
                await manager.broadcast_to_room(room_id, {
                    "type": "chat_message",
                    "sender": data.get("sender_name", "Anonim"),
                    "text": data.get("text", ""),
                    "file_url": data.get("file_url"),
                    "timestamp": data.get("timestamp"),
                })
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        logger.info(f"Mijoz xonadan chiqdi: room_id='{room_id}'")
