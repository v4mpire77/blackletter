# Blackletter Systems – AI Contract Review

Upload → Extract → Summarise → Flag Risks (stubbed, CI-safe).

## Quick Start (Windows)

### Backend
```powershell
cd backend
python -m venv ..\.venv
. ..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:LLM_PROVIDER="stub"
uvicorn app.main:app --reload --port 8000
