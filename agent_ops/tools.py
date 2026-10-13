"""Explicit allow-list of read-only tools; synthetic data only."""
from __future__ import annotations

ALLOWED_TOOLS = {"lookup_order", "lookup_shipping", "lookup_artwork"}


def use_tool(name: str, case: dict) -> dict:
    if name not in ALLOWED_TOOLS:
        raise ValueError(f"Tool not allowed: {name}")
    return {
        "lookup_order": lambda: dict(case["order"]),
        "lookup_shipping": lambda: dict(case["shipping"]),
        "lookup_artwork": lambda: dict(case["artwork"]),
    }[name]()


def select_tools(intent: str) -> list[str]:
    """Fixed tool whitelist means no unconstrained model tool execution."""
    return {
        "shipping_exception": ["lookup_order", "lookup_shipping"],
        "artwork_review": ["lookup_order", "lookup_artwork"],
        "address_change": ["lookup_order", "lookup_shipping"],
        "billing_dispute": ["lookup_order"],
        "no_issue": ["lookup_order", "lookup_shipping"],
    }[intent]
