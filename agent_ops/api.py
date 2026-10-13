"""Local-only demonstration API. No external writes, no customer data."""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .data import get_case, list_cases
from .engine import run_case
from .eval import evaluate
from .models import RunRequest, DecisionRequest
from . import store


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.initialize()
    yield


app = FastAPI(title="AgentOps Reference | Frank Yip", version="0.1.0", lifespan=lifespan)
STATIC = Path(__file__).with_name("dashboard.html")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(STATIC, media_type="text/html")


@app.get("/api/health")
def health():
    return {"status": "ok", "synthetic_data_only": True, "external_writes": False}


@app.get("/api/cases")
def cases():
    return list_cases()


@app.get("/api/cases/{case_id}")
def case_detail(case_id: str):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Synthetic case not found")
    return case


@app.post("/api/cases/{case_id}/run")
def execute(case_id: str, body: RunRequest):
    try:
        return run_case(case_id, body.idempotency_key)
    except LookupError:
        raise HTTPException(status_code=404, detail="Synthetic case not found")


@app.get("/api/actions")
def actions():
    return store.list_actions()


@app.get("/api/actions/{action_id}/audit")
def audit(action_id: str):
    if not store.get_action(action_id):
        raise HTTPException(status_code=404, detail="Action not found")
    return store.audits(action_id)


@app.post("/api/actions/{action_id}/decision")
def review(action_id: str, body: DecisionRequest,
           x_demo_role: str = Header(default="viewer")):
    # This is *not authentication*. For local role-policy demonstrations only;
    # production use requires real session/OIDC authentication at the gateway.
    try:
        return store.decide(action_id, decision=body.decision, role=x_demo_role, note=body.note)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except LookupError:
        raise HTTPException(status_code=404, detail="Action not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@app.get("/api/evaluation")
def evaluation():
    return evaluate()
