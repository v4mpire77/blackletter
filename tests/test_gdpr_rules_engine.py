# isort: skip_file
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.app.services import (
    Playbook,
    RulesConfig,
    analyze_document,
    segment_clauses,
)


def test_segment_clauses_basic():
    text = "1. First clause\nSome text\n2. Second clause\nMore text"
    clauses = segment_clauses(text)
    assert len(clauses) == 2
    assert clauses[0]["id"] == "1"
    assert clauses[1]["id"] == "2"


def test_analyze_document_rules_and_vague_terms():
    contract_text = (
        "1. Data Protection\n"
        "The parties agree to comply with all applicable data protection laws including the GDPR."
        " The Processor shall implement appropriate technical and organizational measures to protect personal data.\n"
        "2. Confidentiality\n"
        "Each party shall use reasonable efforts to maintain the confidentiality of the other party's information."
    )

    rules_json = {
        "rules": [
            {
                "id": "GDPR_DATA_PROCESSING",
                "description": "Data Processing Clause (GDPR Article 28)",
                "primary_keywords": ["personal data", "processing", "data protection"],
                "aliases": ["GDPR", "Data Processing Agreement"],
                "severity": "High",
            },
            {
                "id": "GDPR_BREACH_NOTIFICATION",
                "description": "Personal Data Breach Notification (GDPR Article 33)",
                "primary_keywords": ["72 hours", "breach", "notify"],
                "aliases": ["data breach", "security incident"],
                "severity": "High",
            },
        ]
    }
    rules_conf = RulesConfig.model_validate(rules_json)

    playbook_dict = {
        "organization": "ACME Corp",
        "enable_vague_terms_scan": True,
        "rules": {"GDPR_BREACH_NOTIFICATION": {"severity": "Medium"}},
    }
    playbook_conf = Playbook.model_validate(playbook_dict)

    issues = analyze_document("DOC123", contract_text, rules_conf, playbook_conf)

    rule_issues = {i.rule_id: i for i in issues if i.rule_id != "VAGUE_TERM"}

    assert rule_issues["GDPR_DATA_PROCESSING"].status == "found"
    assert rule_issues["GDPR_DATA_PROCESSING"].clause_path == "1"
    assert rule_issues["GDPR_BREACH_NOTIFICATION"].status == "missing"
    assert rule_issues["GDPR_BREACH_NOTIFICATION"].severity == "Medium"

    vague = [i for i in issues if i.rule_id == "VAGUE_TERM"]
    assert any("reasonable" in v.snippet.lower() for v in vague)


def test_vague_term_multiple_occurrences():
    text = "The processor shall make reasonable efforts to comply and respond within a reasonable time."

    rules_conf = RulesConfig.model_validate({"rules": []})
    playbook = Playbook.model_validate({"enable_vague_terms_scan": True})

    issues = analyze_document("DOC456", text, rules_conf, playbook)

    reasonable_occurrences = [
        i
        for i in issues
        if i.rule_id == "VAGUE_TERM" and "reasonable" in i.snippet.lower()
    ]
    assert len(reasonable_occurrences) == 2
