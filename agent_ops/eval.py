"""Golden-set offline evaluation for five synthetic scenarios."""
from __future__ import annotations

from .data import CASES
from .planner import rules_intent
from .policy import resolve

EXPECTED = {
    "SYN-1001": ("shipping_exception", "draft_ready"),
    "SYN-1002": ("artwork_review", "pending_review"),
    "SYN-1003": ("no_issue", "no_action"),
    "SYN-1004": ("address_change", "pending_review"),
    "SYN-1005": ("billing_dispute", "pending_review"),
}


def evaluate() -> dict:
    details = []
    for key, (intent, status) in EXPECTED.items():
        got = rules_intent(CASES[key])
        got_status = resolve(got)["status"]
        details.append({"case_id": key, "expected": intent, "predicted": got,
                        "status_expected": status, "status_predicted": got_status,
                        "passed": got == intent and got_status == status})
    passed = sum(item["passed"] for item in details)
    return {"passed": passed, "total": len(details), "accuracy": passed / len(details),
            "mode": "deterministic policy baseline; NOT an LLM performance claim", "cases": details}
