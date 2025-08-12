# Blackletter Systems - AI Contract Review

Simple, fast contract review using AI. Upload → Extract → Summarise → Show risks.

## Quick Start (Windows)

### Backend Setup

```powershell
cd blackletter\backend
python -m venv ..\.venv
. ..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
setx OPENAI_API_KEY "<YOUR_KEY>"
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```powershell
cd frontend
npm install
setx NEXT_PUBLIC_API_URL "http://localhost:8000"
npm run dev
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
POST http://localhost:8000/api/review
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.pdf"
Content-Type: application/pdf

< ./test.pdf
------WebKitFormBoundary--
```

## Next Steps

1. Add clause heuristics (termination, assignment, rent review, liability)
2. Redline docx export
3. Add playbook YAML and score risks against it
4. Logging + basic analytics
