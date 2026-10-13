"""Intentionally synthetic, deterministic fixtures; not customer or company data."""
from __future__ import annotations

from copy import deepcopy

CASES = {
    "SYN-1001": {
        "case_id": "SYN-1001", "title": "Shipment hasn't moved", "customer": "Casey Example",
        "flags": {"address_change_requested": False, "payment_disputed": False}, "order": {"status": "fulfilled", "currency": "USD", "total": 46.50, "destination": "US", "age_days": 11},
        "shipping": {"carrier_status": "in_transit", "days_since_scan": 8, "estimated_days": 4},
        "artwork": {"proof_status": "approved", "revision_count": 1},
        "request": "I haven't received my order and tracking hasn't moved.",
    },
    "SYN-1002": {
        "case_id": "SYN-1002", "title": "Artwork proof needs review", "customer": "Avery Sample",
        "flags": {"address_change_requested": False, "payment_disputed": False}, "order": {"status": "proof_pending", "currency": "USD", "total": 79.00, "destination": "CA", "age_days": 2},
        "shipping": {"carrier_status": "not_dispatched", "days_since_scan": 0, "estimated_days": 0},
        "artwork": {"proof_status": "needs_review", "revision_count": 3},
        "request": "The colors on the revised proof still look wrong.",
    },
    "SYN-1003": {
        "case_id": "SYN-1003", "title": "Order delivered", "customer": "Jordan Example",
        "flags": {"address_change_requested": False, "payment_disputed": False}, "order": {"status": "delivered", "currency": "USD", "total": 28.00, "destination": "UK", "age_days": 6},
        "shipping": {"carrier_status": "delivered", "days_since_scan": 1, "estimated_days": 0},
        "artwork": {"proof_status": "approved", "revision_count": 0},
        "request": "Thank you, my order has arrived.",
    },
    "SYN-1004": {
        "case_id": "SYN-1004", "title": "Address change requested", "customer": "Taylor Example",
        "flags": {"address_change_requested": True, "payment_disputed": False}, "order": {"status": "processing", "currency": "USD", "total": 128.00, "destination": "US", "age_days": 1},
        "shipping": {"carrier_status": "not_dispatched", "days_since_scan": 0, "estimated_days": 0},
        "artwork": {"proof_status": "approved", "revision_count": 0},
        "request": "Can you change the shipping address on this order?",
    },
    "SYN-1005": {
        "case_id": "SYN-1005", "title": "Possible duplicate payment", "customer": "Morgan Sample",
        "flags": {"address_change_requested": False, "payment_disputed": True}, "order": {"status": "paid", "currency": "USD", "total": 92.00, "destination": "AU", "age_days": 1},
        "shipping": {"carrier_status": "not_dispatched", "days_since_scan": 0, "estimated_days": 0},
        "artwork": {"proof_status": "approved", "revision_count": 0},
        "request": "I may have been charged twice. Please refund the extra amount.",
    },
}


def get_case(case_id: str) -> dict | None:
    case = CASES.get(case_id)
    return deepcopy(case) if case else None


def list_cases() -> list[dict]:
    return [{"case_id": row["case_id"], "title": row["title"], "request": row["request"]} for row in CASES.values()]
