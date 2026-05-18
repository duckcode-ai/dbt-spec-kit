"""Tests for spec -> plan -> tasks lifecycle validation."""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from dbt_specify.cli import main
from dbt_specify.lifecycle import validate_lifecycle


def test_validate_project_accepts_traced_artifacts(tmp_path: Path) -> None:
    project = _write_lifecycle_project(tmp_path)
    report = validate_lifecycle(project)
    assert report.exit_code == 0, report.to_markdown()


def test_validate_project_rejects_unapproved_plan(tmp_path: Path) -> None:
    project = _write_lifecycle_project(tmp_path, spec_status="draft")
    report = validate_lifecycle(project)
    assert report.exit_code == 1
    assert "PLAN_BEFORE_SPEC_APPROVAL" in report.to_markdown()


def test_validate_project_cli(tmp_path: Path) -> None:
    project = _write_lifecycle_project(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["validate", "project", "--target", str(project)])
    assert result.exit_code == 0, result.output
    assert "dbt-specify project validation" in result.output


def _write_lifecycle_project(tmp_path: Path, spec_status: str = "approved") -> Path:
    project = tmp_path / "project"
    spec_dir = project / "specs" / "001-customer-mart"
    spec_dir.mkdir(parents=True)
    (spec_dir / "spec.md").write_text(
        "# Customer mart\n\n"
        "**Status:** " + spec_status + "\n\n"
        "## Acceptance criteria\n\n"
        "- AC1: The system shall produce `dim_customers`.\n"
        "- AC2: When a source customer is deleted, the system shall preserve history.\n"
    )
    (spec_dir / "plan.md").write_text(
        "# Plan\n\n"
        "**Status:** approved\n\n"
        "## Architecture\nAC1 AC2\n\n"
        "## Files to add\nAC1\n\n"
        "## Files to modify\n(none)\n\n"
        "## Files to delete\n(none)\n\n"
        "## Tests\nAC1 AC2\n\n"
        "## Downstream impact\nAC1 AC2\n"
    )
    (spec_dir / "tasks.md").write_text(
        "# Tasks\n\n"
        "**Status:** in progress\n\n"
        "## Task list\n\n"
        "- [ ] **T-01** — Build dim_customers.\n"
        "  - **Done when:** dbt build runs.\n"
        "  - **Validates:** AC1, AC2\n"
    )
    return project
