import pytest

from agent_ops import store


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENT_OPS_DB", str(tmp_path / "test.sqlite3"))
    monkeypatch.setenv("AGENT_PLANNER", "deterministic")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    store.initialize()
