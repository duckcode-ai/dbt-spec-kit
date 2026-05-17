"""Tests for the init command (Phase A: smoke tests; Phase B fills the rest)."""
from __future__ import annotations

from click.testing import CliRunner

from dbt_specify.cli import main
from dbt_specify.templates_loader import asset_dir, load_template


def test_asset_dir_resolves_all_known_kinds() -> None:
    """Every kind named in templates_loader must resolve to an on-disk directory.

    This is the cheap integration test for T-08: it catches missing packaged
    asset directories (which would otherwise only fail at `init` time).
    """
    for kind in ("memory", "templates", "presets", "skills", "commands"):
        path = asset_dir(kind)
        assert path.is_dir(), f"asset kind '{kind}' did not resolve to a directory"


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
