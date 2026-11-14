"""Routes an AI task to a model identifier based on the requesting user's
plan tier. This is intentionally a static table for now (Phase 5 moves it
into admin-configurable DB rows per Section 22D of the spec) but every
caller already goes through `resolve_model`, so swapping the lookup for a
database query later won't change any call sites.

Tiers exist so free/cheap plans are routed to small, inexpensive models and
paid plans unlock stronger ones -- the mechanism that makes a free tier
survivable on AI cost.
"""

TIER_ECONOMY = "economy"
TIER_STANDARD = "standard"
TIER_PREMIUM = "premium"

# task_name -> {tier: model_identifier}
# Model identifiers are provider-qualified strings; the actual provider
# adapter layer (Phase 5) resolves these against configured credentials.
_TASK_MODELS: dict[str, dict[str, str]] = {
    "resume_parsing": {
        TIER_ECONOMY: "gemini-flash",
        TIER_STANDARD: "gemini-flash",
        TIER_PREMIUM: "claude-sonnet",
    },
    "ats_analysis": {
        TIER_ECONOMY: "gemini-flash",
        TIER_STANDARD: "claude-haiku",
        TIER_PREMIUM: "claude-sonnet",
    },
    "resume_tailoring": {
        TIER_ECONOMY: "claude-haiku",
        TIER_STANDARD: "claude-sonnet",
        TIER_PREMIUM: "claude-opus",
    },
    "interview_evaluation": {
        TIER_ECONOMY: "claude-haiku",
        TIER_STANDARD: "claude-sonnet",
        TIER_PREMIUM: "claude-opus",
    },
}

# Credit cost per task, independent of tier -- the tier changes which model
# is used (and therefore the provider's real $ cost to us), not what the
# user is charged in credits.
_TASK_COSTS: dict[str, int] = {
    "resume_parsing": 1,
    "ats_analysis": 2,
    "resume_tailoring": 5,
    "interview_evaluation": 5,
}


class UnknownTaskError(Exception):
    pass


def resolve_model(task: str, tier: str) -> str:
    if task not in _TASK_MODELS:
        raise UnknownTaskError(f"Unknown AI task: {task}")
    tier_map = _TASK_MODELS[task]
    return tier_map.get(tier, tier_map[TIER_ECONOMY])


def task_cost(task: str) -> int:
    if task not in _TASK_COSTS:
        raise UnknownTaskError(f"Unknown AI task: {task}")
    return _TASK_COSTS[task]
