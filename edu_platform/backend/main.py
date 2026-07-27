import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from db import init_db

# DOMAIN ROUTERS
from users.router import router as users_router
from schools.router import router as schools_router
from courses.router import router as courses_router
from videos.router import router as videos_router
from crm.router import router as crm_router
from payments.router import router as payments_router
from notifications.router import router as notifications_router
from homeworks.router import router as homeworks_router

app = FastAPI(
    title="Exode Education & ERP Platform API",
    description="Multi-tenant online school platform backend API",
    version="2.0.0"
)

# CORS MIDDLEWARE (Allows frontend running on any port/domain to interact with backend API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUDE API ROUTERS WITH /api/v1 PREFIX
app.include_router(users_router, prefix="/api/v1/users", tags=["Users & Auth"])
app.include_router(schools_router, prefix="/api/v1/schools", tags=["Schools & Multi-Tenancy"])
app.include_router(courses_router, prefix="/api/v1/courses", tags=["Courses & Modules"])
app.include_router(videos_router, prefix="/api/v1/videos", tags=["Kinescope Video Integration"])
app.include_router(crm_router, prefix="/api/v1/crm", tags=["Kommo CRM Integration"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["Telegram Admin Payments"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Gmail Free SMTP Notifications"])
app.include_router(homeworks_router, prefix="/api/v1/homeworks", tags=["Homework & Practice Submissions"])

# REALTIME WEBSOCKET CONNECTION MANAGER
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.websocket("/ws/chat/{client_id}")
async def websocket_chat_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Exode ERP Backend API ishlamoqda",
        "docs": "/docs",
        "version": "2.0.0"
    }
