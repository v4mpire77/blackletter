"""GDPR rules engine for contract analysis.

This module segments contract text into clauses and checks each clause
against GDPR rules defined in a JSON configuration, optionally applying
organization-specific overrides from a YAML playbook. It can also detect
vague terms that may require review.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Configuration models
# ---------------------------------------------------------------------------


class Rule(BaseModel):
    """Definition of a single GDPR rule."""

    id: str
    description: str
    primary_keywords: List[str]
    aliases: List[str] = Field(default_factory=list)
    severity: str = "Medium"


class RulesConfig(BaseModel):
    """Container for a list of rules."""

    rules: List[Rule]


class RuleOverride(BaseModel):
    """Override settings for a specific rule in a playbook."""

    enabled: Optional[bool] = None
    severity: Optional[str] = None
    add_keywords: List[str] = Field(default_factory=list)
    add_aliases: List[str] = Field(default_factory=list)


class Playbook(BaseModel):
    """Organization-specific playbook settings."""

    organization: Optional[str] = None
    enable_vague_terms_scan: Optional[bool] = None
    rules: Dict[str, RuleOverride] = Field(default_factory=dict)


class Issue(BaseModel):
    """Result of a rule evaluation or vague term detection."""

    id: str
    doc_id: str
    rule_id: str
    clause_path: Optional[str]
    snippet: str
    citation: Optional[str]
    rationale: str
    severity: str
    status: str
    raw_matches: Dict[str, List[str]]
    rule_scores: Dict[str, bool]


# ---------------------------------------------------------------------------
# Clause segmentation
# ---------------------------------------------------------------------------


CLAUSE_PATTERN = re.compile(
    r"^(?P<cid>(?:(?:Section|Article|Clause)\s+)?\d+(?:\.\d+)*\.?)",
    flags=re.IGNORECASE | re.MULTILINE,
)


def segment_clauses(text: str) -> List[Dict[str, Optional[str]]]:
    """Split raw contract text into clauses using heading heuristics.

    Args:
        text: Contract text.

    Returns:
        List of clauses with ``id`` and ``text`` keys. If no headings are
        found, a single clause with ``id=None`` is returned containing the
        entire text.
    """

    clauses: List[Dict[str, Optional[str]]] = []
    matches = list(CLAUSE_PATTERN.finditer(text))
    if not matches:
        clauses.append({"id": None, "text": text.strip()})
        return clauses

    for idx, match in enumerate(matches):
        cid = match.group("cid").rstrip(".")
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        clause_text = text[start:end].strip()
        clauses.append({"id": cid, "text": clause_text})
    return clauses


# ---------------------------------------------------------------------------
# GDPR analysis
# ---------------------------------------------------------------------------


DEFAULT_VAGUE_TERMS = [
    "reasonable",
    "reasonably",
    "undue delay",
    "promptly",
    "as soon as possible",
    "as soon as practicable",
    "best efforts",
    "commercially reasonable",
    "material",
    "substantial",
    "substantially",
    "appropriate",
    "if appropriate",
    "adequate",
    "satisfactory",
    "sufficient",
]


def _compile_patterns(terms: List[str]) -> List[re.Pattern[str]]:
    return [
        re.compile(r"\b" + re.escape(t) + r"\b", flags=re.IGNORECASE) for t in terms
    ]


def analyze_document(
    doc_id: str,
    text: str,
    rules_config: RulesConfig,
    playbook: Optional[Playbook] = None,
) -> List[Issue]:
    """Analyze ``text`` against GDPR ``rules_config``.

    Args:
        doc_id: Identifier for the analyzed document.
        text: Full contract text.
        rules_config: Configuration of GDPR rules.
        playbook: Optional organization-specific overrides.

    Returns:
        List of ``Issue`` objects describing rule matches or missing clauses and
        any detected vague terms.
    """

    clauses = segment_clauses(text)
    issues: List[Issue] = []
    full_text_lower = text.lower()
    playbook = playbook or Playbook()
    overrides = playbook.rules

    for rule in rules_config.rules:
        if rule.id in overrides and overrides[rule.id].enabled is False:
            continue

        effective_sev = overrides.get(rule.id, RuleOverride()).severity or rule.severity

        keywords = [kw.lower() for kw in rule.primary_keywords]
        aliases = [al.lower() for al in rule.aliases]
        if rule.id in overrides:
            keywords += [kw.lower() for kw in overrides[rule.id].add_keywords]
            aliases += [al.lower() for al in overrides[rule.id].add_aliases]

        kw_patterns = _compile_patterns(keywords)
        alias_patterns = _compile_patterns(aliases)

        found = False
        found_clause_id: Optional[str] = None
        snippet = ""
        matched_terms: List[str] = []

        for i, clause in enumerate(clauses):
            context_parts: List[str] = []
            for j in range(i - 2, i + 3):
                if 0 <= j < len(clauses):
                    context_parts.append(clauses[j]["text"])
            context_text = " ".join(context_parts).lower()

            found_kw = any(p.search(context_text) for p in kw_patterns)
            found_al = any(p.search(context_text) for p in alias_patterns)
            if found_kw or found_al:
                found = True
                found_clause_id = clause["id"]
                clause_text = clause["text"].strip()
                snippet = clause_text[:200] + ("..." if len(clause_text) > 200 else "")
                for p, term in zip(kw_patterns, keywords):
                    if p.search(context_text):
                        matched_terms.append(term)
                for p, term in zip(alias_patterns, aliases):
                    if p.search(context_text):
                        matched_terms.append(term)
                break

        status = "found" if found else "missing"
        rationale = (
            f"Clause covers requirement: {rule.description}"
            if found
            else f"No clause found covering: {rule.description}"
        )

        issue = Issue(
            id=f"{doc_id}_{rule.id}",
            doc_id=doc_id,
            rule_id=rule.id,
            clause_path=found_clause_id,
            snippet=snippet,
            citation=None,
            rationale=rationale,
            severity=effective_sev,
            status=status,
            raw_matches={"keywords": matched_terms},
            rule_scores={
                "primary_found": any(term in keywords for term in matched_terms),
                "alias_found": any(term in aliases for term in matched_terms),
            },
        )
        issues.append(issue)

    if playbook.enable_vague_terms_scan:
        extra_vagues = []
        if "VAGUE_TERMS_EXTRA" in playbook.rules:
            extra_vagues = [
                t.lower() for t in playbook.rules["VAGUE_TERMS_EXTRA"].add_keywords
            ]
        vague_terms = [t.lower() for t in DEFAULT_VAGUE_TERMS] + extra_vagues

        for term in vague_terms:
            pattern = re.compile(re.escape(term), flags=re.IGNORECASE)
            for match in pattern.finditer(full_text_lower):
                idx = match.start()
                snippet_start = max(0, idx - 40)
                snippet_end = min(len(text), idx + len(term) + 40)
                vague_snip = text[snippet_start:snippet_end].strip()
                issues.append(
                    Issue(
                        id=f"{doc_id}_VAGUE_{term}_{idx}",
                        doc_id=doc_id,
                        rule_id="VAGUE_TERM",
                        clause_path=None,
                        snippet=vague_snip + ("..." if snippet_end < len(text) else ""),
                        citation=None,
                        rationale=f"Vague term '{term}' found, which may cause ambiguity",
                        severity="Low",
                        status="review",
                        raw_matches={"term": [term]},
                        rule_scores={"vague_term_found": True},
                    )
                )

    return issues
