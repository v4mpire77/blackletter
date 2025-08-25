# Blackletter GDPR Processor‑Obligations Checker — Context Engineering Implementation

This project is a complete, context-engineered implementation for automated GDPR processor obligations review, designed for clarity, compliance, and continuous improvement.

---

## 🚀 Quickstart

### 1. **Setup**

```powershell
git clone https://github.com/v4mpire77/blackletter.git
cd blackletter
.\scripts\dev-setup.ps1
# Edit .env with your Supabase credentials
```

### 2. **Run All Services**

```powershell
.\scripts\docker-up.ps1
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### 3. **Migrate Database**

```powershell
.\scripts\db-migrate.ps1 -CreateTables
```

### 4. **Validate Context Engineering Compliance**

```powershell
.\tools\context_engineering.ps1 -Action test
```

---

## 🧩 Architecture Overview

- **Frontend:** Next.js 14 (App Router, Tailwind, shadcn/ui, Supabase)
- **Backend:** FastAPI (async), Celery worker, Redis (broker), Supabase Cloud (Postgres)
- **Workflow:** 202 Accepted async pattern, job polling/status, RESTful APIs
- **PowerShell Scripts:** ASCII-only, Windows-safe, for all dev/ops
- **Testing:** pytest (backend), jest/RTL (frontend), golden fixtures
- **Validation:** Context Engineering Framework (80%+ required to pass)

---

## 📂 Key Files & Structure

```
blackletter/
│
├── backend/
│   ├── app/
│   │   ├── core/config.py
│   │   ├── models/schemas.py
│   │   ├── routers/jobs.py
│   │   └── services/job_service.py
│   ├── workers/
│   │   ├── celery_app.py
│   │   └── tasks.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app/upload/page.tsx
│   ├── app/dashboard/page.tsx
│   ├── app/lib/api.ts
│   ├── package.json
│   └── tailwind.config.js
│
├── scripts/
│   ├── dev-setup.ps1
│   ├── docker-up.ps1
│   └── db-migrate.ps1
│
├── tools/
│   └── context_engineering.ps1
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🛡️ Compliance & Testing

- **Context Engineering Framework:**  
  - Run `.\tools\context_engineering.ps1 -Action test`  
  - Must score ≥80% for build to pass

- **Backend:**  
  - `pytest` with fixtures in `backend/tests/fixtures/processor_obligations/`

- **Frontend:**  
  - `jest` with React Testing Library

---

## 📝 Golden Fixture Example

```json name=backend/tests/fixtures/processor_obligations/dpa_missing_subproc.golden.json
{
  "job_id": "fixture-job-id",
  "issues": [
    {
      "id": "uuid-1",
      "doc_id": "fixture-job-id",
      "clause_path": "Section 5.2",
      "type": "GDPR",
      "citation": "UK GDPR Art. 28.3.d",
      "severity": "High",
      "confidence": 0.89,
      "status": "Open",
      "snippet": "No prior written authorisation for subprocessors.",
      "recommendation": "Add requirement for controller approval before engaging subprocessors.",
      "created_at": "2025-08-24T10:00:00Z"
    }
  ],
  "coverage": [
    {
      "article": "Art. 28.3.d",
      "status": "GAP",
      "details": "Subprocessor authorisation",
      "found_clauses": []
    }
  ],
  "summary": "1 high-severity compliance gap detected. See recommendations.",
  "confidence_score": 0.89,
  "processing_time_seconds": 2.2,
  "metadata": { "test_fixture": true }
}
```

---

## 💡 Context Engineering Memory

- All config/secrets from `.env` — never hardcoded
- No local Postgres container — uses **Supabase Cloud**
- 202 Accepted async API pattern (Location header for job status)
- PowerShell scripts are ASCII-only, Windows Defender-friendly
- Build/test/validate scripts must run on Windows without modification
- All endpoints and models reflect build guides and agents.md
- Golden fixtures and compliance tooling are provided

---

## 🔗 References

- See `/00-pre-brief.md`, `/03-build-guide.md`, `/CONTExt APPLYED FULL GUIDE .txt`, `/agents.md` for requirements and architecture.

---

**Happy Context Engineering!**