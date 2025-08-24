# isort: skip_file
"""Services package for Blackletter contract analysis."""

# Export commonly used services
from .gdpr_rules_engine import (
    Issue,
    Playbook,
    Rule,
    RuleOverride,
    RulesConfig,
    analyze_document,
    segment_clauses,
)

__all__ = [
    "Rule",
    "RulesConfig",
    "RuleOverride",
    "Playbook",
    "Issue",
    "segment_clauses",
    "analyze_document",
]
