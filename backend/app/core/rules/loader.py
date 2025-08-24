"""Load rulebook YAML files."""
from importlib import resources
from pathlib import Path
from typing import Dict

import yaml


def load(playbook_id: str) -> Dict[str, dict]:
    """Load rules for the given playbook. Stub implementation."""
    package_path = resources.files(__package__)
    rule_file = package_path / f"{playbook_id}.yml"
    if not rule_file.exists():
        return {}
    with rule_file.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
