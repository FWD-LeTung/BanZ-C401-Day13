# Individual Contribution Report — Nguyen Duc Si

## Team Info
- **Group**: BanZ
- **Repository**: https://github.com/FWD-LeTung/BanZ-C401-Day13
- **Role**: Member D — SLO, Alert Configuration & Data Enrichment
- **Git Author**: Sitito
- **Email**: superbox6996@gmail.com
- **Commit**: `4fdb1e7`
- **Branch**: `si` (merged via PR #2)

---

## 1. Tasks Completed

### 1.1 SLO Configuration
**File**: `config/slo.yaml`
**Commit**: `4fdb1e7` — `data test`

- Defined 4 Service Level Indicators (SLIs) with objectives and targets:

| SLI | Objective | Target | Note |
|---|---|---:|---|
| `latency_p95_ms` | < 2000ms | 99.5% | P95 under 2s for FAQ retrieval + response |
| `error_rate_pct` | < 1% | 99.0% | Low error rate for customer-facing queries |
| `daily_cost_usd` | < $1.0/day | 100% | Budget spike detection with mock LLM |
| `quality_score_avg` | > 0.80 | 95.0% | FAQ answers match expected keywords |

- Set rolling window to 28 days for all SLIs
- Service identifier: `faq-store-support`

### 1.2 Alert Rules Configuration
**File**: `config/alert_rules.yaml`

- Configured 3 symptom-based alert rules:

| Alert Name | Severity | Condition | Owner |
|---|---|---|---|
| `faq_retrieval_slowdown` | P2 | latency_p95_ms > 3000 for 10m | team-oncall |
| `faq_service_errors` | P1 | error_rate_pct > 5 for 5m | team-oncall |
| `token_cost_spike` | P2 | hourly_cost_usd > 2x_baseline for 15m | finops-owner |

- Each alert includes: severity, condition, type, owner, runbook link, and description

### 1.3 Alert Runbooks
**File**: `docs/alerts.md`

- Wrote detailed runbooks for all 3 alert scenarios:
  - **FAQ Retrieval Slowdown**: Root cause checklist (rag_slow toggle, trace review, network latency), immediate mitigation (disable toggle, cache answers), long-term fix (optimize indexing, preload docs)
  - **FAQ Service Errors**: Root cause checklist (tool_fail toggle, error_type grouping), immediate mitigation (disable toggle, fallback message, retry), long-term fix (circuit breaker, graceful degradation)
  - **Token Cost Spike**: Root cause checklist (cost_spike toggle, tokens_out distribution), immediate mitigation (disable toggle, truncate response), long-term fix (pre-compute templates, prompt caching)

### 1.4 Dashboard Specification
**File**: `docs/dashboard-spec.md`

- Specified 6 required dashboard panels with chart types, metrics, SLO lines, thresholds, and purpose:
  1. FAQ Request Traffic (line area)
  2. Response Latency Distribution (multi-line P50/P95/P99)
  3. Error Rate & Type Breakdown (line + stacked bar)
  4. Cost & Token Usage (dual-axis)
  5. Answer Quality Score (line/area)
  6. Safety & Incident Status (stat card + timeline)

### 1.5 Test Data Enrichment
**Files**: `app/mock_rag.py`, `data/sample_queries.jsonl`, `data/expected_answers.jsonl`, `data/incidents.json`

- Enhanced the mock RAG corpus with domain-specific FAQ content (refund, shipping, warranty, payment, order)
- Added keyword-based retrieval routing for 5 categories
- Provided 20 sample queries covering all FAQ categories including PII-containing messages
- Created 10 expected answer entries with `must_include` keyword validation

---

## 2. Technical Highlights

### SLO Design Philosophy
SLOs are designed around **customer impact**, not internal metrics:
- Latency P95 targets the **user experience** of waiting for an FAQ answer
- Error rate targets **service availability** for customer-facing queries
- Cost budget targets **financial sustainability** of the LLM-powered system
- Quality score targets **answer relevance** — the core value proposition

### Alert Severity Mapping
- **P1** (critical): Service errors — customers cannot get answers, revenue impact
- **P2** (high): Latency and cost — degraded experience or budget burn, but service still functional

### Runbook Structure
Each runbook follows a consistent pattern: root cause checklist → immediate mitigation → long-term fix. This enables both rapid incident response and systematic improvement.

---

## 3. Evidence Summary

| Criterion | Evidence |
|---|---|
| Code authorship | Commit `4fdb1e7` — author: Sitito |
| Files owned | `config/slo.yaml`, `config/alert_rules.yaml`, `docs/alerts.md`, `docs/dashboard-spec.md`, `data/*` |
| PR | Branch `si`, merged via PR #2 |
| Runbook quality | 3 complete runbooks with checklists, mitigations, and long-term fixes |

---

## 4. Self-Assessment

| Rubric Item | Max | Claimed | Justification |
|---|---:|---:|---|
| Individual Report (B1) | 20 | 18 | Comprehensive SLO/alert design with rationale, complete runbooks |
| Git Evidence (B2) | 20 | 17 | 1 commit with 9 files modified, clear ownership of observability config |
| **Subtotal** | **40** | **35** | |
