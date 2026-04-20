import json
import os
import tempfile

from app.logging_config import write_audit_log


def test_write_audit_log_creates_file(tmp_path, monkeypatch) -> None:
    audit_path = tmp_path / "audit.jsonl"
    monkeypatch.setattr("app.logging_config.AUDIT_LOG_PATH", audit_path)

    write_audit_log("test_action", correlation_id="req-abc", user_id_hash="hash123")

    lines = audit_path.read_text().strip().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["audit_action"] == "test_action"
    assert record["correlation_id"] == "req-abc"
    assert record["user_id_hash"] == "hash123"
    assert "ts" in record


def test_write_audit_log_appends(tmp_path, monkeypatch) -> None:
    audit_path = tmp_path / "audit.jsonl"
    monkeypatch.setattr("app.logging_config.AUDIT_LOG_PATH", audit_path)

    write_audit_log("action_1")
    write_audit_log("action_2")

    lines = audit_path.read_text().strip().splitlines()
    assert len(lines) == 2


def test_write_audit_log_with_detail(tmp_path, monkeypatch) -> None:
    audit_path = tmp_path / "audit.jsonl"
    monkeypatch.setattr("app.logging_config.AUDIT_LOG_PATH", audit_path)

    write_audit_log("chat_request", detail={"feature": "qa", "session_id": "s01"})

    record = json.loads(audit_path.read_text().strip())
    assert record["detail"]["feature"] == "qa"
    assert record["detail"]["session_id"] == "s01"
