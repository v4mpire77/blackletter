# Deploy to Render

This document shows manual steps to create services on Render and the environment variables required.

## Services to create

1. Backend (FastAPI)
   - Name: blackletter-backend
   - Branch: main
   - Root directory: `backend`
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Health check path: `/health`

2. RAG API (optional, separate service)
   - Name: blackletter-rag
   - Branch: main
   - Root directory: repository root (or `.`)
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `uvicorn rag.api:app --host 0.0.0.0 --port $PORT`
   - Health check path: `/health` (ensure `rag.api` exposes a health endpoint)

## Required environment variables

- `GEMINI_API_KEY` = <your key> (secret)
- `NEXT_PUBLIC_API_URL` = https://<blackletter-backend>.onrender.com
- `NEXT_PUBLIC_RAG_URL` = https://<blackletter-rag>.onrender.com
- Any other variables your deployment needs (TESSERACT_CMD, DB URLs, etc.)

## Notes

- Render will use `runtime.txt` to decide Python version. Ensure it exists and contains `python-3.11.9`.
- Use `gunicorn` + `uvicorn` workers for production if desired; add `gunicorn` to `backend/requirements.txt` and update start command accordingly.

## Troubleshooting

- If build fails, check the build logs for missing packages and add them to `backend/requirements.txt`.
- If app fails to start, check logs for traceback and missing env vars.

***

Remember to enable auto-deploy if you want Render to deploy on each push to the chosen branch.
