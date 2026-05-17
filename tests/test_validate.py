"""Tests for the validate command."""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from dbt_specify.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_validate_accepts_ears_spec(tmp_path: Path) -> None:
    spec = tmp_path / "spec.md"
    spec.write_text(
        "# Test spec\n\n"
        "## Acceptance criteria\n\n"
        "- AC1: The system shall ship a CLI.\n"
        "- AC2: When init runs, the system shall create .dbt-specify/.\n"
    )
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(spec)])
    assert result.exit_code == 0


def test_validate_rejects_non_ears_spec(tmp_path: Path) -> None:
    spec = tmp_path / "spec.md"
    spec.write_text(
        "# Test spec\n\n"
        "## Acceptance criteria\n\n"
        "- We want a CLI.\n"
        "- It should create .dbt-specify/ sometimes.\n"
    )
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(spec)])
    assert result.exit_code != 0
    assert "do not match" in result.output


def test_validate_against_valid_fixture() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(FIXTURES / "valid_spec.md")])
    assert result.exit_code == 0, result.output


def test_validate_against_invalid_fixture() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(FIXTURES / "invalid_spec_non_ears.md")])
    assert result.exit_code != 0
    assert "do not match" in result.output


def test_validate_warns_when_no_ac_section(tmp_path: Path) -> None:
    spec = tmp_path / "spec.md"
    spec.write_text("# Spec without ACs\n\nThis spec forgot its Acceptance Criteria section.\n")
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(spec)])
    assert result.exit_code != 0
    assert "no Acceptance Criteria section" in (result.output + (result.stderr or ""))
