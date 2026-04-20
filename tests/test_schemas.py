import pytest
from pydantic import ValidationError

from app.schemas import ChatRequest, ChatResponse


def test_chat_request_valid() -> None:
    req = ChatRequest(user_id="u01", session_id="s01", message="Hello")
    assert req.feature == "qa"


def test_chat_request_empty_message_rejected() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(user_id="u01", session_id="s01", message="")


def test_chat_response_fields() -> None:
    resp = ChatResponse(
        answer="test",
        correlation_id="req-abc",
        latency_ms=100,
        tokens_in=50,
        tokens_out=80,
        cost_usd=0.001,
        quality_score=0.85,
    )
    assert resp.correlation_id == "req-abc"
    assert resp.quality_score == 0.85
