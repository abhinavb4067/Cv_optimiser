from fastapi import APIRouter, Depends

from app.core.permissions import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary(current_user: User = Depends(get_current_user)):
    """Placeholder summary. Populated with real data in later phases
    (resumes, applications, subscriptions, AI usage)."""
    return {
        "user_id": str(current_user.id),
        "total_uploaded_resumes": 0,
        "total_generated_resumes": 0,
        "saved_jobs": 0,
        "upcoming_interviews": 0,
        "subscription_plan": None,
        "remaining_ai_credits": 0,
    }
