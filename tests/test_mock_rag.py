import pytest

from app.incidents import STATE
from app.mock_rag import retrieve


def _reset_state() -> None:
    for k in STATE:
        STATE[k] = False


def test_retrieve_refund() -> None:
    _reset_state()
    docs = retrieve("How do I get a refund?")
    assert len(docs) == 2
    assert any("refund" in d.lower() for d in docs)


def test_retrieve_shipping() -> None:
    _reset_state()
    docs = retrieve("When will my delivery arrive?")
    assert len(docs) == 2
    assert any("delivery" in d.lower() for d in docs)


def test_retrieve_no_match() -> None:
    _reset_state()
    docs = retrieve("Tell me a joke")
    assert len(docs) == 1
    assert "fallback" in docs[0].lower()


def test_retrieve_tool_fail_raises() -> None:
    _reset_state()
    STATE["tool_fail"] = True
    with pytest.raises(RuntimeError, match="Vector store timeout"):
        retrieve("refund")
    STATE["tool_fail"] = False
