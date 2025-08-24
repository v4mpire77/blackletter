"""Report generation service."""
from pathlib import Path
from typing import List


def render(issues: List[dict], output_dir: Path) -> Path:
    """Create HTML/PDF reports. Stub implementation."""
    return output_dir / "report.html"
