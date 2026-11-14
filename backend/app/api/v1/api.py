from fastapi import APIRouter

from app.api.v1.routes import admin, ai_tasks, auth, dashboard, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(dashboard.router)
api_router.include_router(admin.router)
api_router.include_router(ai_tasks.router)
