# 01 — Repo Map (Pointers)

**Context:** Implement GDPR Processor‑Obligations Checker.

## Relevant Files (reuse)
- `backend/routers/contracts.py` → `/review` endpoint stub (wire analyzer here).
- `frontend/app/upload/page.tsx` → Upload flow entry point.
- `frontend/app/dashboard/page.tsx` (or `/dashboard`) → Issues table & charts.
- `uk_contract_review_compliance_analysis_dashboard_react_tailwind_shadcn_recharts.jsx` → Dashboard component (issue type & fields).

## Gaps / Where to wire
- **Analyzer service**: add `backend/app/services/analyzer.py` with `analyze_processor_obligations(text) -> list[Issue]`.
- **Schemas**: add `backend/app/models/schemas.py` with `Issue` pydantic model (mirrors frontend `Issue`).
- **Coverage map**: add `backend/app/services/coverage.py` for Art. 28 checklist → OK/Partial/GAP.
- **Routes**: extend `contracts.py` to call analyzer and return `Issue[]` + coverage.
- **Tests**: create fixtures under `backend/tests/fixtures/processor_obligations/*.txt|.pdf` and unit tests under `backend/tests/test_processor_obligations.py`.

## Code Stubs (proposed paths)
- `backend/app/services/analyzer.py`
- `backend/app/services/coverage.py`
- `backend/app/models/schemas.py`
- `backend/tests/test_processor_obligations.py`
