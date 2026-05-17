"""Tests for the init command (Phase A: smoke tests; Phase B fills the rest)."""
from __future__ import annotations

from click.testing import CliRunner

from dbt_specify.cli import main
from dbt_specify.templates_loader import load_template


def test_load_template_spec_smoke() -> None:
    """templates_loader can load the packaged spec template."""
    content = load_template("spec")
    assert "Acceptance criteria" in content
    assert "EARS" in content


def test_cli_help_lists_three_subcommands() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0, result.output
    assert "init" in result.output
    assert "validate" in result.output
    assert "version" in result.output


def test_cli_version_prints_package_version() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output
