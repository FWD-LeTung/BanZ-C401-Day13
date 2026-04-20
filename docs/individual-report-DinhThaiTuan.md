# Individual Contribution Report — DinhThaiTuan

## Team Info
- **Group**: BanZ
- **Repository**: https://github.com/FWD-LeTung/BanZ-C401-Day13
- **Role**: Member C — Testing, Audit Logging & PII Bug Fix
- **Branch**: `feat/testing-audit-pii-fix`
- **Commit**: `c75a95f`

---

## 1. Tasks Completed

### 1.1 Audit Logging System (Bonus Feature)
**Files**: `app/logging_config.py`, `app/main.py`

- Implemented `write_audit_log()` function that writes structured audit records to a separate file (`data/audit.jsonl`), independent from the main application logs
- Each audit record includes: ISO timestamp, action type, correlation_id, user_id_hash, and a detail payload
- Integrated audit logging into all relevant endpoints:
  - `/chat`: logs `chat_request`, `chat_response`, and `chat_error` events
  - `/incidents/{name}/enable`: logs `incident_enabled`
  - `/incidents/{name}/disable`: logs `incident_disabled`
- The audit log path is configurable via `AUDIT_LOG_PATH` environment variable (defined in `.env.example`)

**Why this matters**: Audit logs provide a tamper-evident record of all user interactions and system state changes, separate from operational logs. This is a security and compliance best practice.

### 1.2 PII Regex Bug Fix
**File**: `app/pii.py`

- **Bug**: The `phone_vn` pattern `\b(?:\+84|0)\d{9,10}\b` failed to match phone numbers starting with `+84` because `\b` (word boundary) does not trigger before the `+` character
- **Impact**: Numbers like `+84901234567` were silently caught by the `bank_account` pattern instead, producing incorrect redaction labels (`REDACTED_BANK_ACCOUNT` instead of `REDACTED_PHONE_VN`)
- **Fix**: Changed the pattern to `(?:\+84|0)\d{9,10}\b` — removed the leading `\b` so the regex engine can match `+84` at any position
- Verified with dedicated test case `test_scrub_phone_vn_plus84`

### 1.3 Test Suite Expansion (2 → 39 tests)
**Files**: `tests/test_pii.py`, `tests/test_metrics.py`, `tests/test_middleware.py`, `tests/test_audit_logging.py`, `tests/test_incidents.py`, `tests/test_schemas.py`, `tests/test_mock_rag.py`

| Test File | # Tests | What It Covers |
|---|---:|---|
| `test_pii.py` | 13 | Email, phone (0xx & +84), credit card (with/without spaces), passport, multi-PII, no-PII, summarize truncation, summarize PII scrub, hash determinism, hash uniqueness |
| `test_metrics.py` | 7 | Percentile (basic, empty, single), record_request traffic/snapshot, multiple requests P95, record_error breakdown, empty snapshot defaults |
| `test_middleware.py` | 4 | Auto-generated correlation ID, preserve incoming `x-request-id`, response time header, unique IDs across requests |
| `test_audit_logging.py` | 3 | File creation, append behavior, detail payload serialization |
| `test_incidents.py` | 5 | Enable/disable known incidents, KeyError on unknown, status returns all flags |
| `test_schemas.py` | 3 | Valid ChatRequest defaults, empty message rejection, ChatResponse field access |
| `test_mock_rag.py` | 4 | Category matching (refund, shipping), no-match fallback, tool_fail RuntimeError |

### 1.4 Code Quality Improvement
**File**: `app/main.py`

- Extracted `hash_user_id(body.user_id)` and `request.state.correlation_id` into local variables (`uid_hash`, `cid`) to avoid redundant computation (was called 3x per request)

### 1.5 Blueprint Report
**File**: `docs/blueprint-template.md`

- Filled in all previously empty sections: team metadata, SLO table, all 3 incident RCA scenarios (rag_slow, tool_fail, cost_spike), individual contributions for all team members, and bonus items

---

## 2. Technical Deep Dive

### Audit Logging Architecture
```
Request → CorrelationIdMiddleware → chat endpoint
                                      ├── write_audit_log("chat_request")  → data/audit.jsonl
                                      ├── agent.run()
                                      ├── structlog.info("response_sent")  → data/logs.jsonl
                                      └── write_audit_log("chat_response") → data/audit.jsonl
```

Audit logs are intentionally separate from operational logs because:
- They serve different audiences (security/compliance vs. engineering/debugging)
- They have different retention and access policies
- They should not be mixed with high-volume application telemetry

### PII Pattern Ordering
The PII patterns are applied sequentially. The ordering matters because broader patterns (like `bank_account: \d{9,12}`) can match substrings that should be caught by more specific patterns (like `phone_vn`). The fix ensures `phone_vn` runs before `bank_account` and matches correctly.

---

## 3. Evidence Summary

| Criterion | Evidence |
|---|---|
| Code authorship | Commit `c75a95f` on branch `feat/testing-audit-pii-fix` |
| Tests pass | 39/39 tests passing (`python -m pytest tests/ -v`) |
| Audit logs work | Verified via `test_audit_logging.py` — writes real JSONL to disk |
| PII fix verified | `test_scrub_phone_vn_plus84` confirms `+84901234567` → `REDACTED_PHONE_VN` |
| PR created | PR on `feat/testing-audit-pii-fix` → `main` |

---

## 4. Self-Assessment

| Rubric Item | Max Points | Claimed | Justification |
|---|---:|---:|---|
| Individual Report Quality (B1) | 20 | 18 | Detailed report with technical depth, architecture explanation, and RCA scenarios |
| Git Evidence (B2) | 20 | 18 | Clear commit with 13 files changed, +437 lines. Traceable audit logging feature, bug fix, and comprehensive test suite |
| Bonus: Audit Logs | +2 | +2 | Separate audit trail with structured records |
| **Subtotal** | **40+2** | **38** | |
