# 00 — Pre‑Brief Summary

**Module:** GDPR Processor‑Obligations Checker  
**Date:** 2025-08-24 06:25 UTC  
**Owner:** Omar

## Summary (from intake)
- **Problem:** Automatically detect gaps in processor obligations in vendor contracts (Art. 28).  
- **User stories:**  
  - As a reviewer, I want flagged Art. 28(3) gaps with <3% false negatives so I don’t miss compliance obligations.  
  - As a partner, I want a one‑page report that I can share with clients within 10 minutes.  
- **Inputs/Outputs:** PDF/DOCX → extracted text/clauses → `Issue[]` with citations and recommendations.  
- **Scope boundaries:** Out: OCR sophistication, multilingual; In: UK GDPR focus, DPAs/MSAs in English.  
- **Compliance anchors:** UK GDPR Art. 28(1)–(3)(a)‑(h), Art. 32; DPA 2018 selected parts; ICO guidance (processor obligations).  
- **Performance targets:** p95 latency ≤ 60s per doc; cost ≤ £0.10/doc (LLM tokens); precision ≥ 0.85; recall ≥ 0.90 on Art. 28 gaps.  
- **Integration points:** `backend/routers/contracts.py` (review endpoint); dashboard issues table; CSV export.  
- **Constraints:** **Windows‑only** run cmds; no external DB in MVP; pgvector later; Gemini/OpenAI swappable.  
- **Definition of Done:**  
  - Detects missing/weak clauses for Art. 28(3)(a)‑(h) with citations.  
  - Returns structured `Issue[]` and coverage map (OK/Partial/GAP).  
  - Test fixtures pass; thresholds met.  
- **Open risks:** Ambiguity in clause wording; hallucinations; coverage drift across templates.

## To‑Research Checklist
- [ ] Confirm minimal Art. 28(3) obligations list + acceptance wordings.  
- [ ] Map weak‑language heuristics (e.g., “reasonable”, “discretion”, “may”).  
- [ ] Choose chunking strategy (section headers + 1000–1200 token limit).  
- [ ] Select embedding/storage (pgvector later; in‑memory for MVP).  
- [ ] Design eval set (10 public DPAs; synthetic hard negatives).  
