from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import get_current_user
from app.models.user import User
from app.services.credit_service import get_usage_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Resume/job/interview counters are still placeholders until those
    modules land in later phases; subscription and credit data is real."""
    usage = get_usage_summary(db, current_user)
    return {
        "user_id": str(current_user.id),
        "total_uploaded_resumes": 0,
        "total_generated_resumes": 0,
        "saved_jobs": 0,
        "upcoming_interviews": 0,
        "subscription_plan": usage["plan_name"],
        "remaining_ai_credits": usage["remaining"],
        "credit_reset_period": usage["credit_reset_period"],
        "ai_model_tier": usage["ai_model_tier"],
    }
