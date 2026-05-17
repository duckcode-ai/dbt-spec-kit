"""Shared pytest fixtures."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def minimal_dbt_project(tmp_path: Path) -> Path:
    """Create a minimal dbt project directory and return its path."""
    project_dir = tmp_path / "dbt_proj"
    project_dir.mkdir()
    (project_dir / "dbt_project.yml").write_text(
        "name: test_project\nversion: '1.0.0'\nprofile: test\n"
    )
    (project_dir / "models").mkdir()
    return project_dir
