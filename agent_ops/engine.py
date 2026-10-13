"""Read-only agent workflow: observe -> plan -> tools -> policy -> persist."""
from __future__ import annotations

from .data import get_case
from .models import RunResult
from .planner import plan
from .policy import resolve
from .store import get_by_key, create_action
from .tools import select_tools, use_tool


def run_case(case_id: str, key: str) -> RunResult:
    row = get_by_key(case_id, key)
    if row is not None:
        return RunResult(**row, reused=True)
    case = get_case(case_id)
    if case is None:
        raise LookupError(f"Unknown synthetic case: {case_id}")
    intent, planner = plan(case)
    names = select_tools(intent)
    evidence = {name: use_tool(name, case) for name in names}
    row, reused = create_action(
        case_id=case_id, key=key, intent=intent, policy=resolve(intent),
        tools=names, evidence=evidence, planner=planner,
    )
    return RunResult(**row, reused=reused)
