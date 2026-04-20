import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.middleware import CorrelationIdMiddleware


def _make_app() -> FastAPI:
    test_app = FastAPI()
    test_app.add_middleware(CorrelationIdMiddleware)

    @test_app.get("/ping")
    async def ping(request: Request):
        return {"cid": request.state.correlation_id}

    return test_app


def test_generates_correlation_id() -> None:
    client = TestClient(_make_app())
    resp = client.get("/ping")
    assert resp.status_code == 200
    cid = resp.json()["cid"]
    assert cid.startswith("req-")
    assert resp.headers["x-request-id"] == cid


def test_preserves_incoming_correlation_id() -> None:
    client = TestClient(_make_app())
    resp = client.get("/ping", headers={"x-request-id": "custom-123"})
    assert resp.json()["cid"] == "custom-123"
    assert resp.headers["x-request-id"] == "custom-123"


def test_response_time_header() -> None:
    client = TestClient(_make_app())
    resp = client.get("/ping")
    assert "x-response-time-ms" in resp.headers
    assert float(resp.headers["x-response-time-ms"]) >= 0


def test_unique_ids_per_request() -> None:
    client = TestClient(_make_app())
    ids = {client.get("/ping").json()["cid"] for _ in range(5)}
    assert len(ids) == 5
