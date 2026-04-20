# Individual Contribution Report — Le Thanh Thuong

## Team Info
- **Group**: BanZ
- **Repository**: https://github.com/FWD-LeTung/BanZ-C401-Day13
- **Role**: Member B — Tracing & Enrichment
- **Git Author**: thanhthuong194
- **Email**: thanhthuongnlp@gmail.com
- **Commit**: `96b092a`

---

## 1. Tasks Completed

### 1.1 Logging Context Enrichment
**File**: `app/main.py`
**Commit**: `96b092a` — `feat: enrich logging context and tracing metadata`

- Added `bind_contextvars()` in the `/chat` endpoint to attach rich context to every log line:
  - `user_id_hash` — pseudonymized user identity (SHA-256 hash)
  - `session_id` — session tracking for multi-turn conversations
  - `feature` — feature flag (qa, summary, etc.)
  - `model` — LLM model name used for the request
  - `env` — deployment environment (dev/staging/prod)
- These fields are automatically included in all subsequent structlog calls within the same request context, thanks to `structlog.contextvars`

### 1.2 Tracing Metadata via Langfuse
**File**: `app/agent.py` (enrichment integration)

- The enrichment fields flow into Langfuse traces via `langfuse_context.update_current_trace()`:
  - `user_id` (hashed), `session_id`, `tags` (lab, feature, model)
- Observation-level metadata via `langfuse_context.update_current_observation()`:
  - `doc_count`, `query_preview`, `usage_details` (input/output tokens)

### 1.3 Langfuse Trace Verification
- Verified **23 traces** and **46 observations** captured in Langfuse dashboard (see `screenshots/Screenshot 2026-04-20 181306.png`)
- Traces include: 22 `run` type + 1 `manual_test_t...` type
- Observations tracked by level: DEFAULT and ERROR categories

---

## 2. Technical Highlights

### Context Propagation Architecture
```
/chat endpoint
  → bind_contextvars(user_id_hash, session_id, feature, model, env)
    → log.info("request_received")     ← includes all context fields
    → agent.run()
      → langfuse_context.update_current_trace(user_id, session_id, tags)
      → langfuse_context.update_current_observation(metadata, usage_details)
    → log.info("response_sent")        ← includes all context fields
```

### Why Enrichment Matters
Without enrichment, logs only contain `event` and `level`. With enrichment:
- **Debugging**: Filter logs by `session_id` to trace a user's conversation flow
- **Analytics**: Group by `feature` to compare qa vs summary performance
- **Cost tracking**: `model` field enables per-model cost attribution
- **Security**: `user_id_hash` allows user-level analysis without exposing PII

### Langfuse Evidence
From the dashboard screenshot:
- **23 Total traces** (requirement: >= 10 traces) — **PASSED**
- **46 Observations** — each trace contains ~2 observations (retrieval + generation)
- **$0.00 Total cost** — confirms mock LLM is used (no real API calls)

---

## 3. Evidence Summary

| Criterion | Evidence |
|---|---|
| Code authorship | Commit `96b092a` — author: thanhthuong194 |
| Files modified | `app/main.py`, `pyproject.toml`, `uv.lock` |
| Traces verified | 23 traces on Langfuse (screenshot evidence) |
| PR | Part of `feat/observer-tracing-enrichment` branch, merged via PR #3 |

---

## 4. Self-Assessment

| Rubric Item | Max | Claimed | Justification |
|---|---:|---:|---|
| Individual Report (B1) | 20 | 17 | Clear explanation of enrichment strategy and Langfuse integration |
| Git Evidence (B2) | 20 | 17 | 1 commit modifying core app logic, 23 live traces as proof |
| **Subtotal** | **40** | **34** | |
