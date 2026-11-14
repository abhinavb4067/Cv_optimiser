from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import SessionLocal
from app.services.plan_seed import seed_default_plans

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
    db = SessionLocal()
    try:
        seed_default_plans(db)
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
