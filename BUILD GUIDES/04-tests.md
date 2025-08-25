# 04 — Tests (Fixtures & Commands)

## Fixtures
- `backend/tests/fixtures/processor_obligations/`  
  - `dpa_good.txt` (all (a)-(h) present)  
  - `dpa_missing_subproc.txt` (d weak/missing)  
  - `dpa_vague_breach.txt` (“within a reasonable time”)  
  - `dpa_end_of_processing_missing.txt` (g missing)  
  - `msa_overbroad_disclaimer.txt` (conflicts with statutory duties)

## Golden Outputs
- JSON files under `backend/tests/fixtures/processor_obligations/golden/` with `Issue[]` and coverage arrays.

## Windows — Local Run (Smoke)
```powershell
# Backend
cd backend
python -m venv ..\.venv
. ..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:LLM_PROVIDER="stub"
uvicorn app.main:app --reload --port 8000

# Test analyzer (once wired)
pytest -k processor_obligations -q
```

## CLI Checks
- Fails if any detector returns schema errors.  
- Asserts precision/recall thresholds from golden sets.  
