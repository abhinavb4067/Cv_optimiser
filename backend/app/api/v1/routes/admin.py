from fastapi import APIRouter, Depends

from app.core.permissions import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ping", dependencies=[Depends(require_admin)])
def admin_ping():
    return {"status": "ok", "scope": "admin"}
