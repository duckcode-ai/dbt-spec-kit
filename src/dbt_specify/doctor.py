"""Brownfield onboarding diagnostics."""
from __future__ import annotations

from pathlib import Path

from dbt_specify.lifecycle import relpath
from dbt_specify.reporting import Finding, ValidationReport


def doctor_project(target_dir: Path) -> ValidationReport:
    """Inspect a dbt repo and report adoption gaps without changing files."""
    findings: list[Finding] = []

    dbt_project_yml = target_dir / "dbt_project.yml"
    if not dbt_project_yml.exists():
        findings.append(
            Finding(
                "error",
                "DBT_PROJECT_MISSING",
                "No dbt_project.yml found. Run doctor at a dbt project root.",
                relpath(dbt_project_yml, target_dir),
            )
        )
        return ValidationReport("dbt-specify doctor", tuple(findings))

    checks = [
        (
            target_dir / ".dbt-specify" / "constitution.md",
            "DBT_SPECIFY_MISSING",
            "No .dbt-specify/constitution.md found. Run `dbt-specify init`.",
        ),
        (
            target_dir / "CLAUDE.md",
            "AGENT_CONTEXT_MISSING",
            "No CLAUDE.md found. Agents need project-specific context.",
        ),
        (
            target_dir / "specs",
            "SPECS_DIR_MISSING",
            "No specs/ directory found. New work will not be traceable.",
        ),
        (
            target_dir / "target" / "manifest.json",
            "MANIFEST_MISSING",
            "No target/manifest.json found. Run `dbt parse` for artifact-aware checks.",
        ),
    ]
    for path, code, message in checks:
        if not path.exists():
            findings.append(Finding("warning", code, message, relpath(path, target_dir)))

    models_dir = target_dir / "models"
    if not models_dir.exists():
        findings.append(
            Finding(
                "warning",
                "MODELS_DIR_MISSING",
                "No models/ directory found.",
                relpath(models_dir, target_dir),
            )
        )
    else:
        sql_count = len(list(models_dir.rglob("*.sql")))
        yaml_count = len([*models_dir.rglob("*.yml"), *models_dir.rglob("*.yaml")])
        findings.append(
            Finding(
                "info",
                "MODEL_INVENTORY",
                f"Found {sql_count} SQL model file(s) and {yaml_count} YAML docs/test file(s).",
                relpath(models_dir, target_dir),
            )
        )
        if sql_count and not yaml_count:
            findings.append(
                Finding(
                    "warning",
                    "MODEL_DOCS_TESTS_MISSING",
                    "SQL models exist but no model YAML files were found.",
                    relpath(models_dir, target_dir),
                )
            )

    if not findings:
        findings.append(
            Finding(
                "info",
                "DOCTOR_OK",
                "No adoption gaps found by lightweight doctor checks.",
            )
        )
    return ValidationReport("dbt-specify doctor", tuple(findings))
