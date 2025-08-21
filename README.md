#  Blackletter Systems – AI Contract Review (Gemini-only)

Streamline high-volume lease review with automated contract extraction, summary, and risk detection—all in one place. Built with UK/EU legal compliance in mind (AML, GDPR, SRA).
codex/add-one-click-phone-ready-deploy-4bdqfn
## Option A — One-click "phone-ready" deploy

1. Go to [Render](https://render.com) and create a new **Web Service** on the free plan connected to this GitHub repository.
2. Set the service root to `backend` and add these environment variables:
   - `LLM_PROVIDER=openai`
   - `OPENAI_API_KEY=<your OpenAI key>`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Once deployed, note the public URL (e.g., `https://blackletter-api.onrender.com`) for your phone or frontend.

## Quick Start (Windows)
 main

##  Why Blackletter?

-  Designed for UK property law SMEs.
-  Focused on **compliance-first**, not generic AI features.
-  Reduces clause review time by **60%**+; targets **zero missed compliance flags**.
-  Affordable pricing: **£50–100 per user/month**.

---

##  Quick Start (Windows)

### Backend

```powershell
cd blackletter\backend
python -m venv ..\.venv
..\ .venv\Scripts\Activate.ps1
pip install -r requirements.txt
setx GEMINI_API_KEY "<YOUR_GEMINI_KEY>"
setx GEMINI_MODEL "gemini-1.5-flash" # optional
uvicorn main:app --reload --port 8000
