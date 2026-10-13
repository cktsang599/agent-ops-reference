"""Policy always wins over the LLM. All recommendations are non-executing."""
from __future__ import annotations

POLICY = {
    "shipping_exception": {
        "risk": "low", "status": "draft_ready", "requires_review": False,
        "recommendation": "Draft a shipment-status update for staff review; do NOT send or change shipping data.",
    },
    "artwork_review": {
        "risk": "medium", "status": "pending_review", "requires_review": True,
        "recommendation": "Route artwork proof and revision history to a graphics reviewer; no automatic proof approval.",
    },
    "address_change": {
        "risk": "high", "status": "pending_review", "requires_review": True,
        "recommendation": "Escalate proposed address modification to an authorized operator; never auto-edit an order.",
    },
    "billing_dispute": {
        "risk": "high", "status": "pending_review", "requires_review": True,
        "recommendation": "Escalate potential duplicate payment to finance; never auto-refund or charge.",
    },
    "no_issue": {
        "risk": "none", "status": "no_action", "requires_review": False,
        "recommendation": "No operational intervention needed. Keep audit record only.",
    },
}


def resolve(intent: str) -> dict:
    return dict(POLICY[intent])
