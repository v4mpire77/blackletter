# GDPR Processor‑Obligations Checker – Build Guide

## 1) Purpose & Outcome
Detect missing/weak processor obligations in vendor contracts and return structured issues with citations and suggested redlines.  
**Success metrics / Acceptance tests**
- Flags Art. 28(3)(a)-(h) gaps with **precision ≥ 0.85** and **recall ≥ 0.90** on test set.
- Returns `Issue[]` plus a GDPR coverage map (OK/Partial/GAP) per document.
- p95 latency ≤ 60s/doc; no unhandled exceptions on provided fixtures.

## 2) Inputs & Outputs
**Inputs:** PDF bytes → extracted text (per clause)  
**Outputs:**  
- `Issue[]` with `{id, docId, clausePath, type:"GDPR", citation, severity, confidence, status, snippet, recommendation, createdAt}`  
- `Coverage`: `{ article: string, status: "OK"|"Partial"|"GAP" }[]`

## 3) Architecture & Integration
**Backend (FastAPI)**
- Add `app/models/schemas.py`:
```python
from pydantic import BaseModel, Field
from typing import Literal

class Issue(BaseModel):
    id: str
    doc_id: str
    clause_path: str
    type: Literal["GDPR","Statute","Case Law"] = "GDPR"
    citation: str
    severity: Literal["High","Medium","Low"]
    confidence: float = Field(ge=0, le=1)
    status: Literal["Open","In Review","Resolved"] = "Open"
    snippet: str
    recommendation: str
    created_at: str
```
- Add `app/services/analyzer.py` with `analyze_processor_obligations(text: str) -> tuple[list[Issue], list[dict]]`.
- Add `app/services/coverage.py` with `art28_coverage(findings) -> list[dict]`.
- Wire in `routers/contracts.py` → call analyzer and return JSON: `{ issues: Issue[], coverage: Coverage[] }`.

**Frontend**
- Reuse dashboard `Issue` shape (TypeScript):
```ts
export type Issue = {
  id: string; docId: string; clausePath: string;
  type: "GDPR" | "Statute" | "Case Law";
  citation: string; severity: "High" | "Medium" | "Low";
  confidence: number; status: "Open" | "In Review" | "Resolved";
  snippet: string; recommendation: string; createdAt: string;
};
```
- Add call to `/api/analyze` or existing `/contracts/review` and render results in Issues table + GDPR Coverage Map.

## 4) Implementation Steps
1. **Extraction**: Use `pypdf` to extract text; split by headings (regex: `^(\d+(?:\.\d+)*)\s+`) + 1000–1200 token max chunks.  
2. **Detectors**: For each Art. 28(3) obligation, build a detector:  
   - (a) Processing on documented instructions  
   - (b) Confidentiality  
   - (c) Security (Art. 32)  
   - (d) Subprocessors (prior written authorisation / notice + objection)  
   - (e) Data subject assistance  
   - (f) Breach notification + assistance to controller  
   - (g) Deletion/return of personal data at end of processing  
   - (h) Audits/inspections; info provision  
   Each detector returns: `present/weak/missing`, clause path, snippet, citation, recommendation.
3. **Weak‑language heuristics**: Flag phrases like “may at its discretion”, “commercially reasonable”, “within a reasonable time” → downgrade to **weak**.  
4. **LLM pass (optional MVP)**: Summarise per‑clause and classify for each (a)-(h). Enforce **paragraph‑level citations** and structured schema.  
5. **Coverage Map**: Aggregate detector outputs → OK/Partial/GAP.  
6. **Response**: Build `Issue[]` with stable ids and the coverage array.  
7. **CSV export**: Use existing frontend util; ensure fields align.  
8. **Observability**: Log counts per detector; total tokens; p95 latency.

## 5) Evaluation
**Dataset & fixtures**
- 10 public/synthetic DPAs/MSAs with known ground truth.
- Include hard negatives (ambiguous language; missing subprocessor control).

**Metrics**
- Precision/Recall per detector; overall macro‑average.
- Latency (p50/p95); cost per doc (token estimate).

**Pass thresholds**
- Precision ≥ 0.85; Recall ≥ 0.90; p95 ≤ 60s; no schema errors.

## 6) Risks & Mitigations
- **Hallucinations** → Strict schema validation; require clause path + snippet; RAG later.  
- **Ambiguity** → Heuristics + confidence scores; surface as **Medium** severity with reviewer note.  
- **Drift** → Keep detectors data‑driven; store examples for regression tests.

## 7) Ops
- **Config/env**: `LLM_PROVIDER`, `LLM_MODEL`, token caps; Windows‑only runbooks.  
- **Logs/metrics**: counts per (a)-(h), coverage %, timing, token usage.  
- **Cost guardrails**: chunk caps, max tokens, early‑exit on high confidence heuristic matches.

## 8) References
- UK GDPR Art. 28(3), Art. 32; ICO guidance (processor contracts).  
- DPA 2018 (selected sections).  
