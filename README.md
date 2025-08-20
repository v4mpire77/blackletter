# Blackletter Systems - AI Contract Review

Simple, fast contract review using AI. Upload → Extract → Summarise → Show risks.

## Option A — One-click "phone-ready" deploy

1. Go to [Render](https://render.com) and create a new **Web Service** connected to this GitHub repository.
2. Set the service root to `backend` and add the environment variable:
   - `OPENAI_API_KEY=<your OpenAI key>`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Once deployed, note the public URL (e.g., `https://blackletter-api.onrender.com`) for your phone or frontend.

## Quick Start (Windows)

### Backend Setup

```powershell
# Start the default Ollama server (https://ollama.ai)
ollama serve

cd blackletter\backend
python -m venv ..\.venv
. ..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

To use OpenAI instead of Ollama:

```powershell
setx LLM_PROVIDER "openai"
setx OPENAI_API_KEY "<YOUR_KEY>"
```

### Frontend Setup

```powershell
cd frontend
npm install
setx NEXT_PUBLIC_API_URL "http://localhost:8000"
npm run dev
```

### Contract Ingestion

```powershell
.\ingest.ps1 -Path ".\samples" -Out ".\data\chunks.jsonl"
```

### macOS/Linux Tesseract Setup

If you're running the backend on macOS or Linux, ensure the Tesseract
binary is installed and set the `TESSERACT_CMD` environment variable so
`pytesseract` can locate it:

```bash
# macOS (Homebrew)
export TESSERACT_CMD=/usr/local/bin/tesseract

# Linux
export TESSERACT_CMD=/usr/bin/tesseract
```

## System Constraints

- Max file size: 10MB
- File type: PDF only
- Text limit: ~6,000 chars (for LLM processing)

## How We Build

✅ Ship the smallest slice: upload → extract → summarise → show.
✅ Windows-only instructions.
✅ Clear errors, simple UI, one happy path.
❌ Don't add auth/payments yet.
❌ Don't attempt OCR or RAG today.
❌ Don't over-engineer file storage.

## Testing

Use the provided `scripts/test_upload.http` with VS Code REST Client extension to test the API directly:

```http
POST http://localhost:8000/api/contracts
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.pdf"
Content-Type: application/pdf

< ./test.pdf
------WebKitFormBoundary--

### Then fetch findings
GET http://localhost:8000/api/contracts/{id}/findings
```

## Next Steps

1. Add clause heuristics (termination, assignment, rent review, liability)
2. Redline docx export
3. Add playbook YAML and score risks against it
4. Logging + basic analytics
