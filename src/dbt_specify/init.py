"""Implementation of `dbt-specify init` (stub — filled in during Phase B)."""
from __future__ import annotations

from pathlib import Path


def init_project(
    project_name: str,
    warehouse: str,
    target_dir: Path,
    force: bool,
) -> None:
    """Initialize a .dbt-specify/ directory in an existing dbt project.

    Phase A ships only the CLI skeleton; the full implementation lands in Phase B.
    """
    raise NotImplementedError(
        "init command implementation lands in Phase B"
    )
