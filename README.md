# Blackletter Systems - AI Contract Review
![Eval](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/blackletter/blackletter/main/eval/results.json)

![Recall@5](https://img.shields.io/badge/Recall%405-1.00-brightgreen)
![nDCG@5](https://img.shields.io/badge/nDCG%405-1.00-brightgreen)
![Faithfulness](https://img.shields.io/badge/Faithfulness-1.00-brightgreen)

Simple, fast contract review using AI. Upload → Extract → Summarise → Show risks.

## Option A — One-click "phone-ready" deploy

1. Go to [Render](https://render.com) and create a new **Web Service** connected to this GitHub repository.
2. Set the service root to `backend` and set environment variables:
   - `GEMINI_API_KEY=<your Google Gemini key>`
   - `OPENAI_API_KEY=<your OpenAI key>` (optional)
   - `PROVIDER_ORDER=gemini,openai`
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

Set your LLM API keys:

```powershell
setx GEMINI_API_KEY "<YOUR_GEMINI_KEY>"
setx OPENAI_API_KEY "<YOUR_OPENAI_KEY>"  # optional
setx PROVIDER_ORDER "gemini,openai"
```

## Ollama Migration Guide

For cost savings and privacy, you can migrate from cloud LLM providers (Gemini/OpenAI) to local Ollama models:

### 1. Install Ollama
```powershell
# Download and install from https://ollama.ai
ollama --version
```

### 2. Pull a Compatible Model
```powershell
# Recommended models for contract analysis
ollama pull llama3.1      # 4.7GB - good balance of speed/quality
ollama pull llama3.1:8b   # 8GB - higher quality
ollama pull mistral       # 4.1GB - faster alternative
```

### 3. Configure Environment Variables
```powershell
# Switch to Ollama as primary provider
setx LLM_PROVIDER "ollama"
setx OLLAMA_URL "http://localhost:11434"  # default Ollama URL
setx OLLAMA_MODEL "llama3.1"              # or your preferred model

# Optional: Set fallback providers
setx PROVIDER_ORDER "ollama,gemini,openai"
```

### 4. Start Ollama Server
```powershell
ollama serve
```

### 5. Restart Backend
```powershell
# Your backend will now use Ollama for contract analysis
uvicorn main:app --reload --port 8000
```

### Benefits of Ollama Migration
- **Cost Reduction**: No per-token API costs
- **Privacy**: Data stays local, never sent to external APIs
- **Reliability**: No rate limits or API downtime
- **Customization**: Fine-tune models for your specific contract types

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
