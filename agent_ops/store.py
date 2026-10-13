"""Local SQLite idempotency and append-only (application-level) audit log.

Not a full production-grade workflow engine: see LIMITATIONS.md.
"""
from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from uuid import uuid4


def db_path() -> Path:
    return Path(os.getenv("AGENT_OPS_DB", "./demo.sqlite3"))


def connect() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout=5000")
    db.execute("PRAGMA foreign_keys=ON")
    return db


def initialize() -> None:
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS actions (
            action_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            idempotency_key TEXT NOT NULL,
            intent TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            status TEXT NOT NULL,
            risk TEXT NOT NULL,
            requires_review INTEGER NOT NULL,
            tool_calls_json TEXT NOT NULL,
            evidence_json TEXT NOT NULL,
            planner TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(case_id, idempotency_key)
        );
        CREATE TABLE IF NOT EXISTS audits (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id TEXT NOT NULL REFERENCES actions(action_id),
            event_type TEXT NOT NULL,
            actor_role TEXT NOT NULL,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)


def decode(row: sqlite3.Row) -> dict:
    result = dict(row)
    result["tool_calls"] = json.loads(result.pop("tool_calls_json"))
    result["evidence"] = json.loads(result.pop("evidence_json"))
    result["requires_review"] = bool(result["requires_review"])
    return result


def get_by_key(case_id: str, key: str) -> dict | None:
    with connect() as db:
        row = db.execute("SELECT * FROM actions WHERE case_id=? AND idempotency_key=?", (case_id, key)).fetchone()
    return decode(row) if row else None


def get_action(action_id: str) -> dict | None:
    with connect() as db:
        row = db.execute("SELECT * FROM actions WHERE action_id=?", (action_id,)).fetchone()
    return decode(row) if row else None


def create_action(*, case_id: str, key: str, intent: str, policy: dict,
                  tools: list[str], evidence: dict, planner: str) -> tuple[dict, bool]:
    """Atomic insert-or-read idempotency under concurrent requests."""
    action_id = str(uuid4())
    with connect() as db:
        cursor = db.execute("""
          INSERT OR IGNORE INTO actions
          (action_id,case_id,idempotency_key,intent,recommendation,status,risk,
           requires_review,tool_calls_json,evidence_json,planner)
          VALUES (?,?,?,?,?,?,?,?,?,?,?)
          """, (action_id,case_id,key,intent,policy["recommendation"],policy["status"],
                 policy["risk"],int(policy["requires_review"]),json.dumps(tools),
                 json.dumps(evidence),planner))
        created = cursor.rowcount == 1
        row = db.execute("SELECT * FROM actions WHERE case_id=? AND idempotency_key=?", (case_id,key)).fetchone()
        if created:
            db.execute("INSERT INTO audits (action_id,event_type,actor_role,note) VALUES (?,?,?,?)",
                       (row["action_id"], "plan_created", "ops-agent", f"{intent} | {planner}"))
    return decode(row), not created


def decide(action_id: str, *, decision: str, role: str, note: str) -> dict:
    if role != "reviewer":
        raise PermissionError("Only a reviewer may record approval or rejection")
    with connect() as db:
        row = db.execute("SELECT * FROM actions WHERE action_id=?", (action_id,)).fetchone()
        if not row:
            raise LookupError(action_id)
        if row["status"] != "pending_review":
            raise ValueError("Decision requires a pending review")
        status = "approved_for_manual_handling" if decision == "approve" else "rejected"
        # Atomic compare-and-set prevents two reviewers resolving a request twice.
        updated = db.execute("UPDATE actions SET status=? WHERE action_id=? AND status='pending_review'",
                             (status, action_id))
        if updated.rowcount != 1:
            raise ValueError("Review already resolved")
        db.execute("INSERT INTO audits (action_id,event_type,actor_role,note) VALUES (?,?,?,?)",
                   (action_id,f"review_{decision}",role,note))
        latest = db.execute("SELECT * FROM actions WHERE action_id=?", (action_id,)).fetchone()
    return decode(latest)


def list_actions(limit: int = 30) -> list[dict]:
    with connect() as db:
        rows = db.execute("SELECT * FROM actions ORDER BY created_at DESC, rowid DESC LIMIT ?", (limit,)).fetchall()
    return [decode(r) for r in rows]


def audits(action_id: str) -> list[dict]:
    with connect() as db:
        rows = db.execute("SELECT event_id,event_type,actor_role,note,created_at FROM audits WHERE action_id=? ORDER BY event_id",
                          (action_id,)).fetchall()
    return [dict(r) for r in rows]
