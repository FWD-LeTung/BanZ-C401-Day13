# FAQ Store Support System - Observability Lab Report

> **Instruction**: Fill in all sections below. This report is for the mini online store FAQ assistant system. Preserve all tags (e.g., `[GROUP_NAME]`).

## 1. Team Metadata
- [GROUP_NAME]: BanZ
- [REPO_URL]: https://github.com/FWD-LeTung/BanZ-C401-Day13
- [MEMBERS]:
  - Member A: LeTung | Role: Logging & PII Scrubbing
  - Member B: thanhthuong194 | Role: Tracing & Enrichment
  - Member C: Sitito | Role: SLO & Alert Configuration
  - Member D: DinhThaiTuan | Role: Testing, Audit Logging & PII Bug Fix
  - Member E: (Unassigned) | Role: RCA & Demo Lead

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 80/100
- [TOTAL_TRACES_COUNT]: Pending live verification
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: Verified via middleware — every request gets `req-{uuid}` or forwards `x-request-id`
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: Verified via `scrub_event` processor — all payload strings scrubbed before logging
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: Requires Langfuse keys to capture live
- [TRACE_WATERFALL_EXPLANATION]: The `agent.run` span captures doc retrieval + LLM generation; `usage_details` and `metadata` are attached via `langfuse_context.update_current_observation`

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: See `docs/dashboard-spec.md` for panel definitions
- [SLO_TABLE]:
| SLI | Target | Window | Baseline |
|---|---:|---|---:|
| Latency P95 | < 2000ms | 28d | FAQ retrieval + generation time |
| Error Rate | < 1% | 28d | FAQ tool failures + schema validation errors |
| Cost Budget | < $1.0/day | 1d | Mock LLM token estimation |
| Quality Score | > 0.80 | 28d | Heuristic: answer length + keyword match + no redaction leaks |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: 3 alert rules configured in `config/alert_rules.yaml`
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md](../docs/alerts.md)

---

## 4. Incident Response & Root Cause Analysis

### Scenario 1: rag_slow
- [SYMPTOMS_OBSERVED]: p95 latency spike to >3000ms; `mock_rag.retrieve()` adds 2.5s sleep when `STATE["rag_slow"]` is True
- [ROOT_CAUSE_PROVED_BY]: Trace showing slow retrieval span; `latency_ms` field in logs jumps from ~200ms to >2700ms
- [FIX_ACTION]: Disable via `POST /incidents/rag_slow/disable`; optimize corpus indexing
- [PREVENTIVE_MEASURE]: Alert on p95 > 2000ms for 10m (`faq_retrieval_slowdown` rule); preload FAQ corpus

### Scenario 2: tool_fail
- [SYMPTOMS_OBSERVED]: error_rate_pct jumps to >5%; logs show `RuntimeError: Vector store timeout`
- [ROOT_CAUSE_PROVED_BY]: `mock_rag.retrieve()` raises RuntimeError when `STATE["tool_fail"]` is True; error_type logged in request_failed event
- [FIX_ACTION]: Disable via `POST /incidents/tool_fail/disable`; implement fallback answer template
- [PREVENTIVE_MEASURE]: Circuit breaker; `faq_service_errors` alert at error_rate > 5% for 5m

### Scenario 3: cost_spike
- [SYMPTOMS_OBSERVED]: hourly_cost_usd doubles; `tokens_out` per request increases 4x
- [ROOT_CAUSE_PROVED_BY]: `mock_llm.FakeLLM.generate()` multiplies `output_tokens *= 4` when `STATE["cost_spike"]` is True; cost_usd field shows spike in logs
- [FIX_ACTION]: Disable via `POST /incidents/cost_spike/disable`; truncate response to max 200 tokens
- [PREVENTIVE_MEASURE]: `token_cost_spike` alert at hourly_cost > 2x baseline for 15m; pre-compute FAQ templates

---

## 5. Individual Contributions & Evidence

### LeTung (Member A)
- [TASKS_COMPLETED]: Middleware correlation ID implementation, PII scrubbing patterns, structlog configuration with JSON file processor, scrub_event processor, initial project setup
- [EVIDENCE_LINK]: Commits `232ea70` (middleware, PII, sub_event) and `85d6db3` (initial commit)

### thanhthuong194 (Member B)
- [TASKS_COMPLETED]: Enriched logging context with `bind_contextvars` (user_id_hash, session_id, feature, model, env), tracing metadata via `langfuse_context.update_current_trace/observation`
- [EVIDENCE_LINK]: Commit `96b092a` (feat: enrich logging context and tracing metadata)

### Sitito (Member C)
- [TASKS_COMPLETED]: SLO configuration (`config/slo.yaml`), alert rules (`config/alert_rules.yaml`), alert runbooks (`docs/alerts.md`), dashboard spec (`docs/dashboard-spec.md`), test data enrichment
- [EVIDENCE_LINK]: Commit `4fdb1e7` (data test) — PR #2

### DinhThaiTuan (Member D)
- [TASKS_COMPLETED]: 
  - Implemented audit logging system (`write_audit_log` in `logging_config.py`) with separate audit trail in `data/audit.jsonl`
  - Integrated audit log calls into chat endpoint (`app/main.py`): request, response, and error events
  - Fixed PII regex bug: `phone_vn` pattern with `+84` prefix was incorrectly matched by `bank_account` due to `\b` word boundary not matching before `+`
  - Expanded test suite from 2 tests to 39 tests covering all modules:
    - `test_pii.py`: 13 tests (email, phone, credit card, passport, summarize, hash)
    - `test_metrics.py`: 7 tests (percentile, record_request, record_error, snapshot)
    - `test_middleware.py`: 4 tests (correlation ID generation, preservation, response time, uniqueness)
    - `test_audit_logging.py`: 3 tests (file creation, append, detail payload)
    - `test_incidents.py`: 5 tests (enable, disable, unknown key, status)
    - `test_schemas.py`: 3 tests (valid request, empty message rejection, response fields)
    - `test_mock_rag.py`: 4 tests (category matching, fallback, tool_fail error)
- [EVIDENCE_LINK]: See latest commits on current branch

---

## 6. Bonus Items (Optional)
- [BONUS_AUDIT_LOGS]: Implemented separate audit logging to `data/audit.jsonl` via `write_audit_log()`. Each audit record captures timestamp, action type, correlation_id, user_id_hash, and detail payload. Integrated into the `/chat` endpoint for request/response/error tracking.
- [BONUS_COST_OPTIMIZATION]: Mock LLM cost estimation uses per-token pricing ($3/M input, $15/M output). SLO set at <$1.0/day budget.
- [BONUS_CUSTOM_METRIC]: Quality score heuristic in `agent._heuristic_quality()` combining doc match, answer length, keyword overlap, and PII leak penalty.
