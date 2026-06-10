# tests/unit/test_audit_logger.py
import pytest
from datetime import datetime, timedelta
from agent_shield.logging.audit_logger import AuditLogger
from agent_shield.memory.context_pruner import ContextPruner

@pytest.fixture
def logger(tmp_path):
    return AuditLogger(log_dir=tmp_path)

def test_tool_call_logging(logger):
    user_id = "user-123"
    op = "prune_context"
    pruner = ContextPruner(logger=logger)
    pruner.prune(user_id=user_id, context_id="ctx-1")
    entry = logger.get_last_entry()
    assert entry["user_id"] == user_id
    assert entry["operation"] == op
    assert "timestamp" in entry

def test_memory_write_logging(logger):
    user_id = "user-456"
    ctx_id = "ctx-2"
    data = {"key": "value"}
    logger.log_memory_write(user_id, ctx_id, data)
    entry = logger.get_last_entry()
    assert entry["operation"] == "memory_write"
    assert entry["context_id"] == ctx_id
    assert entry["payload_summary"] == str(data)

def test_immutability(logger):
    logger.log_event("test", {})
    with pytest.raises(RuntimeError):
        logger.update_last_entry({"foo": "bar"})

def test_retention_policy(tmp_path):
    logger = AuditLogger(log_dir=tmp_path, retention_days=1)
    old_ts = datetime.utcnow() - timedelta(days=2)
    logger._write_entry({"timestamp": old_ts.isoformat(), "data": "old"})
    logger._purge_old_entries()
    assert not logger._entry_exists(old_ts)

def test_query_endpoint(client, logger):
    # seed entries
    logger.log_event("event1", {"user_id": "u1"})
    logger.log_event("event2", {"user_id": "u2"})
    resp = client.get("/audit-logs?user_id=u1")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["event"] == "event1"