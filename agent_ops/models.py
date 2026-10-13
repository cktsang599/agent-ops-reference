from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

Intent = Literal["shipping_exception", "artwork_review", "address_change", "billing_dispute", "no_issue"]


class RunRequest(BaseModel):
    idempotency_key: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9_.-]+$")


class DecisionRequest(BaseModel):
    decision: Literal["approve", "reject"]
    note: str = Field(default="", max_length=500)


class CandidatePlan(BaseModel):
    intent: Intent
    explanation: str = Field(min_length=3, max_length=400)


class RunResult(BaseModel):
    action_id: str
    case_id: str
    intent: Intent
    recommendation: str
    status: str
    risk: str
    requires_review: bool
    tool_calls: list[str]
    evidence: dict
    planner: str
    reused: bool = False
    # Actions are drafts or review decisions. This demo never sends messages,
    # updates orders, or performs external writes.
