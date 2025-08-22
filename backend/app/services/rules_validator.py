"""
Rules Validator Service

Validates GDPR rules JSON configuration with regex sanity checks.
"""
import json
import re
from typing import List
from pathlib import Path
from ..models import rules as m

def load_rules(path: str) -> m.RuleSet:
    """
    Load and validate GDPR rules from JSON file.
    
    Args:
        path: Path to rules JSON file
        
    Returns:
        Validated RuleSet model
        
    Raises:
        ValueError: If rules are invalid or contain bad regex patterns
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # First pass: Pydantic validation
    rs = m.RuleSet(**data)
    
    # Second pass: Regex compilation checks
    errors: List[str] = []
    for rule in rs.rules:
        for check in rule.checks:
            if hasattr(check, "patterns"):
                for p in getattr(check, "patterns"):
                    try:
                        re.compile(p)
                    except re.error as e:
                        errors.append(f"{rule.id} invalid regex '{p}': {e}")
            
            if check.type == "negation_regex":
                try:
                    re.compile(check.pattern)  # type: ignore
                except re.error as e:
                    errors.append(f"{rule.id} invalid negation_regex '{check.pattern}': {e}")
    
    if errors:
        raise ValueError("\n".join(errors))
        
    return rs

def validate_rules_file(rules_path: str = None) -> bool:
    """
    Validate rules file before API startup.
    
    Args:
        rules_path: Optional path to rules file. If None, uses default path.
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If validation fails
    """
    if rules_path is None:
        rules_path = str(Path(__file__).parent.parent.parent / "rules" / "gdpr_rules.json")
        
    try:
        load_rules(rules_path)
        return True
    except Exception as e:
        raise ValueError(f"Rules validation failed: {str(e)}")

# Example usage:
if __name__ == "__main__":
    try:
        validate_rules_file()
        print("Rules OK")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
