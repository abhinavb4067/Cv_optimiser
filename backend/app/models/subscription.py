import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    monthly_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)

    # Which AI model tier this plan is routed to by default.
    # "economy" -> cheapest/smallest models, "standard" -> mid-tier, "premium" -> frontier models.
    ai_model_tier: Mapped[str] = mapped_column(String(20), default="economy", nullable=False)

    # "lifetime" -> credit_limit is a one-time pool that's never replenished
    #   (fits free plans: a resume isn't touched daily, so a daily/monthly
    #   reset either starves a working session or quietly over-grants).
    # "monthly" -> credit_limit refills every calendar month, for paying
    #   plans where the recurring grant matches the recurring payment.
    credit_reset_period: Mapped[str] = mapped_column(String(20), default="lifetime", nullable=False)
    credit_limit: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("subscription_plans.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    plan: Mapped["SubscriptionPlan"] = relationship("SubscriptionPlan")


class CreditTransaction(Base):
    """One row per credit-consuming (or granted) event. Daily/monthly usage
    is computed by summing these rather than maintaining a separate mutable
    counter, so usage history and enforcement always agree."""

    __tablename__ = "credit_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)  # negative = consumed, positive = granted
    reason: Mapped[str] = mapped_column(String(100), nullable=False)
    model_tier: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )
