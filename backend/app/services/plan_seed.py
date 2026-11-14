from sqlalchemy.orm import Session

from app.models.subscription import SubscriptionPlan
from app.services.model_router import TIER_ECONOMY, TIER_PREMIUM, TIER_STANDARD

DEFAULT_PLANS = [
    {
        "slug": "free",
        "name": "Free",
        "is_free": True,
        "monthly_price": 0,
        "ai_model_tier": TIER_ECONOMY,
        "credit_reset_period": "lifetime",
        "credit_limit": 30,
    },
    {
        "slug": "pro",
        "name": "Pro",
        "is_free": False,
        "monthly_price": 19,
        "ai_model_tier": TIER_STANDARD,
        "credit_reset_period": "monthly",
        "credit_limit": 600,
    },
    {
        "slug": "premium",
        "name": "Premium",
        "is_free": False,
        "monthly_price": 49,
        "ai_model_tier": TIER_PREMIUM,
        "credit_reset_period": "monthly",
        "credit_limit": 3000,
    },
]


def seed_default_plans(db: Session) -> None:
    for plan_data in DEFAULT_PLANS:
        existing = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == plan_data["slug"]).first()
        if existing is None:
            db.add(SubscriptionPlan(**plan_data))
    db.commit()


def get_free_plan(db: Session) -> SubscriptionPlan:
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "free").first()
    if plan is None:
        raise RuntimeError("Free plan is not seeded. Run seed_default_plans() first.")
    return plan
