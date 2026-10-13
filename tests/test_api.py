from fastapi.testclient import TestClient
from agent_ops.api import app


def test_health_and_dashboard():
    with TestClient(app) as client:
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json()["external_writes"] is False
        page = client.get("/")
        assert page.status_code == 200
        assert "Frank Yip" in page.text
        assert "Synthetic data" in page.text


def test_api_run_role_gate_and_audit():
    with TestClient(app) as client:
        r = client.post("/api/cases/SYN-1004/run", json={"idempotency_key": "api-key-1"})
        assert r.status_code == 200
        action = r.json()
        assert action["status"] == "pending_review"
        denied = client.post(f"/api/actions/{action['action_id']}/decision", json={"decision": "approve"})
        assert denied.status_code == 403
        allowed = client.post(
            f"/api/actions/{action['action_id']}/decision",
            json={"decision": "approve", "note": "human review"},
            headers={"X-Demo-Role": "reviewer"},
        )
        assert allowed.status_code == 200
        assert allowed.json()["status"] == "approved_for_manual_handling"
        audit = client.get(f"/api/actions/{action['action_id']}/audit")
        assert len(audit.json()) == 2


def test_404_and_input_validation():
    with TestClient(app) as client:
        assert client.get("/api/cases/NOT-A-CASE").status_code == 404
        assert client.post("/api/cases/SYN-1001/run", json={"idempotency_key": "?"}).status_code == 422
        assert client.post("/api/cases/REAL-123/run", json={"idempotency_key": "test"}).status_code == 404
