import pytest

from app.incidents import STATE, disable, enable, status


def _reset_state() -> None:
    for k in STATE:
        STATE[k] = False


def test_enable_known_incident() -> None:
    _reset_state()
    enable("rag_slow")
    assert STATE["rag_slow"] is True


def test_disable_known_incident() -> None:
    _reset_state()
    STATE["tool_fail"] = True
    disable("tool_fail")
    assert STATE["tool_fail"] is False


def test_enable_unknown_raises() -> None:
    with pytest.raises(KeyError):
        enable("nonexistent")


def test_disable_unknown_raises() -> None:
    with pytest.raises(KeyError):
        disable("nonexistent")


def test_status_returns_copy() -> None:
    _reset_state()
    s = status()
    assert set(s.keys()) == {"rag_slow", "tool_fail", "cost_spike"}
    assert all(v is False for v in s.values())
