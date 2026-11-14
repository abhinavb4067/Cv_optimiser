from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import get_current_user
from app.models.user import User
from app.schemas.ai_task import AiTaskRequest, AiTaskResponse
from app.services.credit_service import CreditError, consume_credits, get_active_subscription, get_usage_summary
from app.services.model_router import UnknownTaskError, resolve_model, task_cost

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/run-task", response_model=AiTaskResponse)
def run_ai_task(data: AiTaskRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Demo endpoint proving the credit + model-tier routing pipeline end to
    end, ahead of the real provider integrations landing in Phase 5. It
    deducts credits and reports which model tier the request would use --
    no actual AI provider is called here."""
    try:
        cost = task_cost(data.task)
    except UnknownTaskError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    subscription = get_active_subscription(db, current_user)
    tier = subscription.plan.ai_model_tier
    model = resolve_model(data.task, tier)

    try:
        consume_credits(db, current_user, cost, reason=data.task, model_tier=tier)
    except CreditError as exc:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(exc))

    summary = get_usage_summary(db, current_user)
    return AiTaskResponse(
        task=data.task,
        model_used=model,
        credits_charged=cost,
        remaining_credits=summary["remaining"],
        credit_reset_period=summary["credit_reset_period"],
    )
