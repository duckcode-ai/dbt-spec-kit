"""Implementation of `dbt-specify validate` (stub — filled in during Phase F)."""
from __future__ import annotations

from pathlib import Path


def validate_spec(spec_path: Path) -> int:
    """Validate that a spec's Acceptance Criteria are EARS-conformant.

    Phase A ships only the CLI skeleton; the full validator lands in Phase F.
    """
    raise NotImplementedError(
        "validate command implementation lands in Phase F"
    )
