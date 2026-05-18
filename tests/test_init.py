"""Tests for the init command."""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from dbt_specify.cli import main
from dbt_specify.init import SUPPORTED_WAREHOUSES
from dbt_specify.templates_loader import asset_dir, load_template


def test_asset_dir_resolves_all_known_kinds() -> None:
    """Every kind named in templates_loader must resolve to an on-disk directory."""
    for kind in ("memory", "templates", "presets", "skills", "commands", "agents"):
        path = asset_dir(kind)
        assert path.is_dir(), f"asset kind '{kind}' did not resolve to a directory"


def test_load_template_spec_smoke() -> None:
    """templates_loader can load the packaged spec template."""
    content = load_template("spec")
    assert "Acceptance criteria" in content
    assert "EARS" in content


def test_cli_help_lists_enterprise_subcommands() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0, result.output
    assert "ci" in result.output
    assert "doctor" in result.output
    assert "init" in result.output
    assert "jira" in result.output
    assert "report" in result.output
    assert "validate" in result.output
    assert "version" in result.output


def test_cli_version_prints_package_version() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["version"])
    assert result.exit_code == 0
    assert "1.3.0" in result.output


def test_init_help_shows_flags() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["init", "--help"])
    assert result.exit_code == 0
    assert "--warehouse" in result.output
    assert "--force" in result.output
    assert "--target" in result.output
    for warehouse in SUPPORTED_WAREHOUSES:
        assert warehouse in result.output


def test_init_creates_dbt_specify_dir(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0, result.output
    assert (minimal_dbt_project / ".dbt-specify").is_dir()
    assert (minimal_dbt_project / ".dbt-specify" / "constitution.md").exists()
    # Templates copied
    assert (minimal_dbt_project / ".dbt-specify" / "templates" / "spec-template.md").exists()
    assert (minimal_dbt_project / ".dbt-specify" / "templates" / "plan-template.md").exists()
    # Commands and skills directories created
    assert (minimal_dbt_project / ".dbt-specify" / "commands").is_dir()
    assert (minimal_dbt_project / ".dbt-specify" / "commands" / "dbt.analyze.md").exists()
    assert (minimal_dbt_project / ".dbt-specify" / "commands" / "dbt.implement-all.md").exists()
    assert (minimal_dbt_project / ".dbt-specify" / "commands" / "dbt.review.md").exists()
    assert (minimal_dbt_project / ".dbt-specify" / "skills").is_dir()
    agents_dir = minimal_dbt_project / ".dbt-specify" / "agents"
    assert agents_dir.is_dir()
    for agent_name in (
        "spec-steward",
        "dbt-architect",
        "warehouse-optimizer",
        "implementation-agent",
        "governance-reviewer",
        "review-agent",
    ):
        assert (agents_dir / f"{agent_name}.md").exists()
    # CLAUDE.md is written when none exists
    assert (minimal_dbt_project / "CLAUDE.md").exists()
    # specs/ directory created
    assert (minimal_dbt_project / "specs").is_dir()


def test_init_appends_snowflake_additions(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    constitution = (minimal_dbt_project / ".dbt-specify" / "constitution.md").read_text()
    assert "BEGIN SNOWFLAKE ADDITIONS" in constitution
    assert "clustering" in constitution.lower()


def test_init_fails_without_dbt_project_yml(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(tmp_path)],
    )
    assert result.exit_code != 0
    assert "dbt_project.yml" in result.output


def test_init_refuses_to_overwrite_without_force(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code != 0
    assert "already exists" in result.output


def test_init_force_overwrites_existing(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    # Drop a sentinel inside the existing .dbt-specify/ dir
    sentinel = minimal_dbt_project / ".dbt-specify" / "sentinel.txt"
    sentinel.write_text("old")
    result = runner.invoke(
        main,
        [
            "init", "test",
            "--warehouse", "snowflake",
            "--target", str(minimal_dbt_project),
            "--force",
        ],
    )
    assert result.exit_code == 0, result.output
    assert not sentinel.exists(), "--force should have wiped the previous .dbt-specify/"


def test_init_databricks_preset(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "databricks", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0, result.output
    constitution = (minimal_dbt_project / ".dbt-specify" / "constitution.md").read_text()
    assert "BEGIN DATABRICKS ADDITIONS" in constitution
    assert "liquid clustering" in constitution.lower()


def test_init_trino_preset(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "trino", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0, result.output
    constitution = (minimal_dbt_project / ".dbt-specify" / "constitution.md").read_text()
    assert "BEGIN TRINO ADDITIONS" in constitution
    # Trino is a federated query engine — that word should appear in the additions.
    text = constitution.lower()
    assert "federation" in text or "federated" in text


def test_init_bigquery_preset(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "bigquery", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0, result.output
    constitution = (minimal_dbt_project / ".dbt-specify" / "constitution.md").read_text()
    plan = (
        minimal_dbt_project / ".dbt-specify" / "templates" / "plan-template.md"
    ).read_text()
    assert "BEGIN BIGQUERY ADDITIONS" in constitution
    assert "partitioning" in constitution.lower()
    assert "BigQuery-specific concerns" in plan


def test_every_supported_warehouse_preset_initializes(tmp_path: Path) -> None:
    runner = CliRunner()
    expected_skill_by_warehouse = {
        "snowflake": "snowflake-clustering-decisions",
        "databricks": "databricks-liquid-clustering-decisions",
        "trino": "trino-federated-query-patterns",
        "bigquery": "bigquery-partitioning-decisions",
        "redshift": "redshift-dist-sort-decisions",
        "postgres": "postgres-index-materialization-decisions",
        "sqlserver": "sqlserver-index-and-incremental-decisions",
        "azure-sql": "azure-sql-service-tier-decisions",
        "mysql": "mysql-oltp-safe-analytics-decisions",
        "duckdb": "duckdb-local-analytics-decisions",
        "motherduck": "motherduck-collaboration-decisions",
        "athena": "athena-partition-file-layout-decisions",
    }
    assert set(expected_skill_by_warehouse) == set(SUPPORTED_WAREHOUSES)

    for warehouse in SUPPORTED_WAREHOUSES:
        project_dir = tmp_path / warehouse
        project_dir.mkdir()
        (project_dir / "dbt_project.yml").write_text(
            "name: test_project\nversion: '1.0.0'\nprofile: test\n"
        )
        (project_dir / "models").mkdir()

        result = runner.invoke(
            main,
            ["init", "test", "--warehouse", warehouse, "--target", str(project_dir)],
        )
        assert result.exit_code == 0, result.output

        constitution = (project_dir / ".dbt-specify" / "constitution.md").read_text()
        plan = (project_dir / ".dbt-specify" / "templates" / "plan-template.md").read_text()
        expected_marker = f"BEGIN {warehouse.upper()} ADDITIONS"
        assert expected_marker in constitution
        assert f"BEGIN {warehouse.upper()} PLAN ADDITIONS" in plan
        assert (
            project_dir
            / ".dbt-specify"
            / "skills"
            / expected_skill_by_warehouse[warehouse]
            / "SKILL.md"
        ).exists()


def test_init_existing_claude_md_writes_suggested_file(minimal_dbt_project: Path) -> None:
    (minimal_dbt_project / "CLAUDE.md").write_text("# pre-existing\n")
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0, result.output
    assert (minimal_dbt_project / "CLAUDE.md").read_text() == "# pre-existing\n"
    assert (minimal_dbt_project / "CLAUDE.md.dbt-specify-suggested").exists()
