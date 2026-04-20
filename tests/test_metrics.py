from app.metrics import percentile, record_error, record_request, snapshot, ERRORS, QUALITY_SCORES, REQUEST_COSTS, REQUEST_LATENCIES, REQUEST_TOKENS_IN, REQUEST_TOKENS_OUT


def _reset_metrics() -> None:
    import app.metrics as m
    m.TRAFFIC = 0
    REQUEST_LATENCIES.clear()
    REQUEST_COSTS.clear()
    REQUEST_TOKENS_IN.clear()
    REQUEST_TOKENS_OUT.clear()
    ERRORS.clear()
    QUALITY_SCORES.clear()


def test_percentile_basic() -> None:
    assert percentile([100, 200, 300, 400], 50) >= 100


def test_percentile_empty() -> None:
    assert percentile([], 95) == 0.0


def test_percentile_single() -> None:
    assert percentile([42], 99) == 42.0


def test_record_request_updates_traffic() -> None:
    _reset_metrics()
    record_request(latency_ms=100, cost_usd=0.001, tokens_in=50, tokens_out=80, quality_score=0.9)
    s = snapshot()
    assert s["traffic"] == 1
    assert s["latency_p50"] == 100.0
    assert s["total_cost_usd"] == 0.001
    assert s["tokens_in_total"] == 50
    assert s["tokens_out_total"] == 80
    assert s["quality_avg"] == 0.9


def test_record_multiple_requests() -> None:
    _reset_metrics()
    for i in range(5):
        record_request(latency_ms=100 * (i + 1), cost_usd=0.001, tokens_in=50, tokens_out=80, quality_score=0.8)
    s = snapshot()
    assert s["traffic"] == 5
    assert s["latency_p95"] >= 400.0


def test_record_error() -> None:
    _reset_metrics()
    record_error("RuntimeError")
    record_error("RuntimeError")
    record_error("TimeoutError")
    s = snapshot()
    assert s["error_breakdown"]["RuntimeError"] == 2
    assert s["error_breakdown"]["TimeoutError"] == 1


def test_snapshot_empty() -> None:
    _reset_metrics()
    s = snapshot()
    assert s["traffic"] == 0
    assert s["avg_cost_usd"] == 0.0
    assert s["quality_avg"] == 0.0
