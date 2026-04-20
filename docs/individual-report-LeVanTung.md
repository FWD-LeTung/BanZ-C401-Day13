# Individual Contribution Report — Le Van Tung

## Team Info
- **Group**: BanZ
- **Repository**: https://github.com/FWD-LeTung/BanZ-C401-Day13
- **Role**: Member A — Logging & PII Scrubbing
- **Git Author**: LeTung / FWD-LeTung
- **Email**: lethanhtung9319@gmail.com
- **Commits**: `232ea70`, `85d6db3`

---

## 1. Tasks Completed

### 1.1 Initial Project Setup
**Commit**: `85d6db3` — `initial commit`

- Set up project scaffolding: `pyproject.toml`, `.python-version`, `main.py`
- Initialized the repository and configured Python environment

### 1.2 Correlation ID Middleware
**File**: `app/middleware.py`
**Commit**: `232ea70` — `middleware, PII, sub_event, 80/100`

- Implemented `CorrelationIdMiddleware` using Starlette's `BaseHTTPMiddleware`
- Auto-generates `req-{uuid}` if no `x-request-id` header is provided
- Forwards incoming `x-request-id` for end-to-end tracing
- Binds `correlation_id` to structlog context via `bind_contextvars()` so all subsequent logs include it
- Attaches `correlation_id` to `request.state` for access in route handlers
- Adds `x-request-id` and `x-response-time-ms` response headers

### 1.3 PII Scrubbing
**File**: `app/pii.py`

- Implemented `scrub_text()` with regex patterns for 8 PII types:
  - Email, CCCD (12-digit citizen ID), credit card, Vietnamese phone (+84/0xx), passport, bank account, Vietnamese address keywords, zip code
- Implemented `summarize_text()` — truncates to max length after PII scrubbing
- Implemented `hash_user_id()` — SHA-256 hash (first 12 chars) for pseudonymization

### 1.4 Structlog Configuration
**File**: `app/logging_config.py`

- Configured structlog pipeline with processors:
  - `merge_contextvars` — pulls correlation_id and other context
  - `add_log_level`, `TimeStamper` (ISO/UTC)
  - `scrub_event` — applies PII scrubbing to all payload strings and event names
  - `JsonlFileProcessor` — writes each log as JSON line to `data/logs.jsonl`
  - `JSONRenderer` — final console output

### 1.5 Main App Integration
**File**: `app/main.py`

- Wired up middleware, logging, and PII scrubbing into FastAPI app
- Added `service` field to all log events for consistent categorization

---

## 2. Technical Highlights

### Correlation ID Flow
```
Client Request
  → x-request-id header (or auto-generated)
    → bind_contextvars(correlation_id=...)
      → All structlog calls include correlation_id
        → Response header x-request-id
```
This enables end-to-end request tracing across logs and traces.

### PII Scrubbing Pipeline
The `scrub_event` processor runs **before** `JsonlFileProcessor`, ensuring no PII is ever written to disk. Pattern ordering matters — more specific patterns (CCCD, credit card, phone) run before broader ones (bank account, zip code).

---

## 3. Evidence Summary

| Criterion | Evidence |
|---|---|
| Code authorship | Commits `232ea70`, `85d6db3` — author: LeTung |
| Files owned | `app/middleware.py`, `app/pii.py`, `app/logging_config.py`, `app/main.py` |
| Validate score | 80/100 (stated in commit message) |
| PR | PR #1 (`letung` → `main`), merged |

---

## 4. Self-Assessment

| Rubric Item | Max | Claimed | Justification |
|---|---:|---:|---|
| Individual Report (B1) | 20 | 18 | Core infrastructure: middleware, PII, structlog — detailed explanation |
| Git Evidence (B2) | 20 | 19 | 2 commits, 6+ files modified, clear ownership of logging pipeline |
| **Subtotal** | **40** | **37** | |
