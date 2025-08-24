# GDPR Processor-Obligations Checker – Build To‑Dos

1. **Backend Foundations**
   1.1 Create Pydantic models (`backend/app/models/schemas.py`).
   1.2 Scaffold rulebook loader and sample YAML (`backend/app/core/rules`).
   1.3 Implement review router (`backend/app/routers/review.py`).
   1.4 Wire router in `backend/app/main.py`.
   1.5 Add service stubs: `ingest.py`, `detect.py`, `judge.py`, `report.py`.
   1.6 Add Celery task `run_review` in `backend/app/workers/tasks.py`.
   1.7 Create Postgres models/tables and migrations.

2. **Frontend Foundations**
   2.1 Define Review types (`frontend/types/review.ts`).
   2.2 Extend API client with review endpoints (`frontend/lib/api.ts`).
   2.3 Scaffold UI components (`frontend/app/(components)/ReviewStatus.tsx`, `IssueDialog.tsx`).
   2.4 Hook upload page to POST `/api/review` and polling.
   2.5 Render issues and download buttons on dashboard.

3. **Processing Pipeline**
   3.1 Implement ingestion (PDF/DOCX → text/OCR).
   3.2 Segment text and run heuristic/embedding detection.
   3.3 Call LLM via adapter for clause judgement.
   3.4 Generate HTML/PDF reports.
   3.5 Persist results, metrics, and artifacts.

4. **Rulebook & Checks**
   4.1 Encode ≥8 Art.28 rules in YAML.
   4.2 Add regex patterns for vague wording.
   4.3 Write unit tests for rule evaluation.

5. **Queues & Events**
   5.1 Configure Celery + Redis, define `contracts.review` queue.
   5.2 Emit progress/completion/error events (SSE optional).

6. **Testing & QA**
   6.1 Unit tests: review endpoints, rulebook loader, service functions.
   6.2 Integration test: upload fixture contract → issues returned.
   6.3 Windows smoke test (backend & frontend run).
   6.4 Achieve ≥80 % coverage.

7. **Security & Compliance**
   7.1 Enforce file size/type limits and virus scanning stub.
   7.2 Ensure encryption at rest (MinIO) and job deletion API.
   7.3 Store hashed prompts + citations for audit trail.

8. **Performance & Monitoring**
   8.1 Track per‑stage latency and cost.
   8.2 Alert on recall <90 % or job errors >2 %.
   8.3 Optimize concurrency for ≥20 parallel jobs.

