"""Tests for dbt artifact validation."""
from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from dbt_specify.cli import main
from dbt_specify.dbt_artifacts import validate_dbt_project


def test_validate_dbt_accepts_manifest_with_docs_tests_and_grain(tmp_path: Path) -> None:
    project = _write_dbt_project_with_manifest(tmp_path)
    report = validate_dbt_project(project)
    assert report.exit_code == 0, report.to_markdown()


def test_validate_dbt_rejects_model_without_test(tmp_path: Path) -> None:
    project = _write_dbt_project_with_manifest(tmp_path, include_test_child=False)
    report = validate_dbt_project(project)
    assert report.exit_code == 1
    assert "MODEL_TEST_MISSING" in report.to_markdown()


def test_validate_dbt_cli_json_report(tmp_path: Path) -> None:
    project = _write_dbt_project_with_manifest(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["report", "--target", str(project), "--format", "json"])
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert data["title"] == "dbt-specify CI report"


def test_ci_requires_manifest(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["ci", "--target", str(minimal_dbt_project)])
    assert result.exit_code == 1
    assert "MANIFEST_MISSING" in result.output


def test_doctor_reports_brownfield_gaps(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["doctor", "--target", str(minimal_dbt_project)])
    assert result.exit_code == 0, result.output
    assert "DBT_SPECIFY_MISSING" in result.output


def _write_dbt_project_with_manifest(
    tmp_path: Path,
    include_test_child: bool = True,
) -> Path:
    project = tmp_path / "dbt_project"
    target = project / "target"
    target.mkdir(parents=True)
    (project / "dbt_project.yml").write_text("name: demo\nversion: '1.0.0'\nprofile: demo\n")
    child_map = {"model.demo.dim_customers": ["test.demo.not_null_dim_customers_customer_id"]}
    if not include_test_child:
        child_map["model.demo.dim_customers"] = []
    manifest = {
        "nodes": {
            "model.demo.dim_customers": {
                "resource_type": "model",
                "name": "dim_customers",
                "description": "One row per customer. Grain: customer_id.",
                "original_file_path": "models/marts/dim_customers.sql",
                "meta": {"grain": "one row per customer"},
            },
            "test.demo.not_null_dim_customers_customer_id": {
                "resource_type": "test",
                "name": "not_null_dim_customers_customer_id",
            },
        },
        "sources": {
            "source.demo.raw_customers": {
                "name": "raw_customers",
                "original_file_path": "models/staging/sources.yml",
                "freshness": {"warn_after": {"count": 12, "period": "hour"}},
                "loaded_at_field": "loaded_at",
            }
        },
        "child_map": child_map,
        "exposures": {
            "exposure.demo.customer_dashboard": {
                "name": "customer_dashboard",
            }
        },
    }
    (target / "manifest.json").write_text(json.dumps(manifest))
    return project
