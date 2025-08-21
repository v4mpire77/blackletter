#  Blackletter Systems – AI Contract Review (Gemini-only)

Streamline high-volume lease review with automated contract extraction, summary, and risk detection—all in one place. Built with UK/EU legal compliance in mind (AML, GDPR, SRA).

---

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
