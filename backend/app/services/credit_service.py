from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.subscription import CreditTransaction, SubscriptionPlan, UserSubscription
from app.models.user import User


class CreditError(Exception):
    pass


def get_active_subscription(db: Session, user: User) -> UserSubscription:
    subscription = db.query(UserSubscription).filter(UserSubscription.user_id == user.id).first()
    if subscription is None:
        raise CreditError("User has no active subscription")
    return subscription


def _consumed_since(db: Session, user_id, since: datetime | None) -> int:
    query = db.query(func.coalesce(func.sum(CreditTransaction.amount), 0)).filter(
        CreditTransaction.user_id == user_id,
        CreditTransaction.amount < 0,
    )
    if since is not None:
        query = query.filter(CreditTransaction.created_at >= since)
    return abs(query.scalar() or 0)


def get_usage_summary(db: Session, user: User) -> dict:
    subscription = get_active_subscription(db, user)
    plan: SubscriptionPlan = subscription.plan

    if plan.credit_reset_period == "monthly":
        window_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        # "lifetime" -> no window; usage is summed over the whole account history.
        window_start = None

    used = _consumed_since(db, user.id, window_start)

    return {
        "plan_slug": plan.slug,
        "plan_name": plan.name,
        "ai_model_tier": plan.ai_model_tier,
        "credit_reset_period": plan.credit_reset_period,
        "credit_limit": plan.credit_limit,
        "used": used,
        "remaining": max(plan.credit_limit - used, 0),
    }


def consume_credits(db: Session, user: User, amount: int, reason: str, model_tier: str | None = None) -> None:
    summary = get_usage_summary(db, user)

    if amount > summary["remaining"]:
        period_label = "ever on this plan" if summary["credit_reset_period"] == "lifetime" else "this month"
        upsell = (
            "Upgrade your plan for more credits."
            if summary["credit_reset_period"] == "lifetime"
            else "Try again next month or upgrade your plan."
        )
        raise CreditError(
            f"AI credit limit reached ({summary['credit_limit']} credits {period_label} on the "
            f"{summary['plan_name']} plan). {upsell}"
        )

    db.add(
        CreditTransaction(
            user_id=user.id,
            amount=-amount,
            reason=reason,
            model_tier=model_tier,
        )
    )
    db.commit()
