from pydantic import BaseModel, ConfigDict


class AiTaskRequest(BaseModel):
    task: str


class AiTaskResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    task: str
    model_used: str
    credits_charged: int
    remaining_credits: int
    credit_reset_period: str
