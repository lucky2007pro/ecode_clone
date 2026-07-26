import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
    description="Multi-tenant online school platform backend API with Clean URLs and Realtime WebSockets",
    version="2.0.0"
)

# CORS MIDDLEWARE
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

# FRONTEND CLEAN URL SERVING MATCHING EXODE.BIZ ROUTES
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/training")
@app.get("/student")
async def serve_student_training():
    return FileResponse(os.path.join(FRONTEND_DIR, "student.html"))

@app.get("/manage/dashboard")
@app.get("/dashboard")
async def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

@app.get("/manage/courses/{course_id}")
@app.get("/course-builder")
async def serve_course_builder(course_id: str = "1"):
    return FileResponse(os.path.join(FRONTEND_DIR, "course-builder.html"))

@app.get("/manage/invoices/{invoice_id}")
@app.get("/payments")
async def serve_payments(invoice_id: str = "1"):
    return FileResponse(os.path.join(FRONTEND_DIR, "payments.html"))

@app.get("/manage/homeworks/{homework_id}")
@app.get("/homework")
async def serve_homework(homework_id: str = "1"):
    return FileResponse(os.path.join(FRONTEND_DIR, "homework.html"))

@app.get("/manage/school/users/{user_id}")
@app.get("/analytics")
async def serve_analytics(user_id: str = "1"):
    return FileResponse(os.path.join(FRONTEND_DIR, "analytics.html"))

@app.get("/manage/school/settings/basic")
@app.get("/customization")
async def serve_customization():
    return FileResponse(os.path.join(FRONTEND_DIR, "customization.html"))

@app.get("/chat")
@app.get("/messenger")
async def serve_messenger():
    return FileResponse(os.path.join(FRONTEND_DIR, "messenger.html"))

@app.get("/courses")
async def serve_courses():
    return FileResponse(os.path.join(FRONTEND_DIR, "courses.html"))

@app.get("/pricing")
async def serve_pricing():
    return FileResponse(os.path.join(FRONTEND_DIR, "pricing.html"))

@app.get("/features")
async def serve_features():
    return FileResponse(os.path.join(FRONTEND_DIR, "features.html"))

@app.get("/docs")
async def serve_docs():
    return FileResponse(os.path.join(FRONTEND_DIR, "docs.html"))

@app.get("/login")
async def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.get("/register")
async def serve_register():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))

# SERVE STATIC ASSETS DIRECTLY AT ROOT IF FILE EXISTS
@app.get("/{file_path:path}")
async def serve_static_file(file_path: str):
    target = os.path.join(FRONTEND_DIR, file_path)
    if os.path.isfile(target):
        return FileResponse(target)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
