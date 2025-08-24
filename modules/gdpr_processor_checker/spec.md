# GDPR Processor-Obligations Checker – Consolidated Spec

## 1. Module Name & Problem
GDPR Processor-Obligations Checker detects gaps and weak language in vendor contracts against UK GDPR Article 28(3) obligations to prevent compliance breaches and reduce manual review time.

## 2. User Stories & Success Metrics
- **Compliance lawyer:** automatically detect mandatory clauses (e.g. breach notification ≤72h) to avoid manual scanning.
- **Managing partner:** receive a traffic-light report with citations and remediation steps for sign-off.
- **Legal ops manager:** vague terms like “reasonable” are flagged for tightening.

**Metrics**
- ≥95 % recall on Article 28 clauses.
- ≤3 % false negatives; ≤10 % false positives.
- ≥60 % reduction in review time.
- 100 % issues include citation or “not found”.
- Zero missed high‑risk obligations.

## 3. Inputs & Outputs
**Inputs**
- PDF/DOCX files (≤10 MB, ≤20 pages), optional metadata: `contract_type`, `jurisdiction`, `playbook_id`.

**Outputs**
- ReviewResult JSON with summary, risk level, Issue list, Metrics, report URLs.
- HTML/PDF report downloads.
- Uniform error model `{ "error": { code, message } }`.

## 4. Scope Boundaries
**In scope**
- File upload pipeline with OCR fallback.
- Clause segmentation, regex heuristics, semantic retrieval (pgvector).
- LLM classification with citations and traffic‑light risk.
- Dashboard with issue table, KPI tiles, CSV export.
- Basic authentication; Postgres + MinIO storage.

**Out of scope (v1)**
- Payments, advanced multi‑tenancy, custom playbook UI, document collaboration, case‑law RAG, employment/AML checks, mobile app.

## 5. Compliance Anchors
- **Art. 28(3):** documented instructions, confidentiality, security, sub‑processor consent, data subject rights assistance, breach notification, DPIA support, deletion/return, audit rights.
- **Art. 32:** security of processing (encryption, resilience, recovery).
- **Arts. 44‑49:** international transfers (IDTA/SCCs/adequacy).
- **Arts. 33‑34:** breach handling support.
- **DPA 2018:** Part 2 s.57, Schedule 1 safeguards for special categories.
- **ICO guidance:** flag vague timing (“reasonable time”), prohibit blanket sub‑processor consent, DSAR assistance free of charge, avoid rights‑waiving disclaimers.

## 6. Performance Targets
- **Accuracy:** recall ≥95 %, false negatives ≤3 %, false positives ≤10 %.
- **Latency:** ≤30 s total for 10‑page DPA (ingest ≤8 s, classify ≤10 s, report ≤5 s).
- **Cost:** ≤£0.15 per 10‑page DPA; ≤1 vCPU & 2 GB RAM per job.
- **Stability:** 99 % jobs without retry; supports 20 concurrent reviews with <5 % latency degradation.
- **Monitoring:** alert if recall <90 %; track cost, latency, precision/recall per job.

## 7. Integration Points
### Backend
- `backend/app/routers/review.py` – POST/GET/DELETE endpoints.
- `backend/app/main.py` – include router under `/api`.
- Services: `ingest.py`, `detect.py`, `judge.py`, `report.py`.
- Workers: `backend/app/workers/tasks.py` Celery task `run_review`.
- Models: `backend/app/models/schemas.py` for Issue, ReviewResult, Metrics.
- Rulebook: YAML files under `backend/app/core/rules/` loaded via `loader.py`.
- Dependencies: pypdf, pytesseract, pdfminer.six, pgvector, sentence‑transformers/OpenAI embeddings, LLM adapter, Celery + Redis, weasyprint/reportlab.

### Frontend
- Pages: `frontend/app/upload/page.tsx`, `frontend/app/dashboard/page.tsx`.
- Components: `frontend/app/(components)/ReviewStatus.tsx`, `frontend/app/(components)/IssueDialog.tsx`.
- API client: `frontend/lib/api.ts`.

### Queue & Events
- Queue `contracts.review`; task `run_review(job_id, tenant_id, playbook_id)`.
- Optional SSE channel `/api/events/{job_id}` with progress/completed/error messages.

### Database & Storage
- Postgres tables: jobs, contract_pages, chunks, issues, artifacts.
- Object storage layout:
  - `uploads/{tenant}/{job_id}/original.pdf`
  - `extracted/{tenant}/{job_id}/pages.json`
  - `reports/{tenant}/{job_id}/report.{html,pdf}`

### Configuration
- Backend `.env`: `POSTGRES_URL`, `REDIS_URL`, `S3_*`, `EMBEDDINGS_PROVIDER`, `LLM_PROVIDER`, `LLM_MODEL`.
- Frontend `.env.local` (Windows): `setx NEXT_PUBLIC_API_URL "http://localhost:8000/api"`.

### CI / QA Hooks
- Unit tests: `backend/tests/test_review_endpoint.py` (mock LLM), `backend/tests/test_rules_yaml.py`.
- Windows smoke test commands for backend & frontend.

## 8. Risks & Mitigations
1. **Hallucinations / false flags** – rulebook-first checks, paragraph citations, QA guardian cross-check.
2. **OCR failures** – pypdf primary, Tesseract fallback, surface explicit errors.
3. **Vague language** – regex patterns flag ambiguous terms as Amber.
4. **International transfers** – explicit checks for IDTA/SCCs; flag “any country” wording.
5. **Scalability** – cap file size, async Celery workers, retries with backoff.
6. **Audit trail** – store hashed prompts + citations, generate PDF/CSV reports.
7. **Security** – encrypt files, 30‑day retention, allow job deletion.
8. **Adoption** – show snippets with citations, traffic‑light risk scores; frame as AI co‑pilot.

## 9. Definition of Done
- Endpoints `/api/review`, `/api/review/{id}`, `/api/review/{id}/report(.pdf)` live.
- Upload PDF/DOCX → job queued → issues render on dashboard.
- ≥8 Article‑28 checks in rulebook; each issue has citation or “not found”.
- HTML/PDF report downloadable.
- Windows smoke runbook passes (backend + frontend).
- Unit & integration tests green (endpoint + rulebook fixtures) with ≥80 % coverage.

## 10. Open Risks & Unknowns
- Regulatory updates to ICO guidance or international transfer rules.
- LLM pricing/latency shifts; OCR failures on poor scans; semantic search misses.
- Lawyer adoption and interpretation of confidence scores.
- Execution risks: founder runway, messy pilot contracts, demand for extra checks.
- Unknowns to validate: cloud vs on‑prem demand, baseline gap rate, ROI threshold, required integrations, cost ceiling feasibility.

