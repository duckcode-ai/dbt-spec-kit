"""Validate dbt project structure and dbt artifacts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dbt_specify.lifecycle import relpath
from dbt_specify.reporting import Finding, ValidationReport


def validate_dbt_project(
    target_dir: Path,
    manifest_path: Path | None = None,
    require_manifest: bool = False,
) -> ValidationReport:
    """Validate dbt-specific enterprise guardrails."""
    findings: list[Finding] = []
    dbt_project_yml = target_dir / "dbt_project.yml"
    if not dbt_project_yml.exists():
        return ValidationReport(
            "dbt artifact validation",
            (
                Finding(
                    "error",
                    "DBT_PROJECT_MISSING",
                    "No dbt_project.yml found. Run this command at a dbt project root.",
                    relpath(dbt_project_yml, target_dir),
                ),
            ),
        )

    resolved_manifest = manifest_path or target_dir / "target" / "manifest.json"
    if not resolved_manifest.exists():
        if require_manifest:
            return ValidationReport(
                "dbt artifact validation",
                (
                    Finding(
                        "error",
                        "MANIFEST_MISSING",
                        "No target/manifest.json found. Run `dbt parse` before CI validation.",
                        relpath(resolved_manifest, target_dir),
                    ),
                ),
            )
        findings.extend(_validate_without_manifest(target_dir))
        return ValidationReport("dbt artifact validation", tuple(findings))

    manifest = _load_manifest(resolved_manifest, target_dir)
    if isinstance(manifest, Finding):
        return ValidationReport("dbt artifact validation", (manifest,))

    findings.extend(_validate_manifest(manifest, resolved_manifest, target_dir))
    return ValidationReport("dbt artifact validation", tuple(findings))


def _validate_without_manifest(target_dir: Path) -> list[Finding]:
    findings: list[Finding] = [
        Finding(
            "warning",
            "MANIFEST_MISSING",
            "No target/manifest.json found. Run `dbt parse` before CI-grade validation.",
            "target/manifest.json",
        )
    ]
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
        return findings

    model_files = sorted(models_dir.rglob("*.sql"))
    if not model_files:
        findings.append(
            Finding(
                "warning",
                "NO_MODEL_SQL",
                "models/ contains no SQL model files.",
                relpath(models_dir, target_dir),
            )
        )
    yaml_files = [*models_dir.rglob("*.yml"), *models_dir.rglob("*.yaml")]
    if model_files and not yaml_files:
        findings.append(
            Finding(
                "warning",
                "NO_MODEL_YAML",
                "models/ has SQL files but no YAML docs/tests files.",
                relpath(models_dir, target_dir),
            )
        )
    return findings


def _load_manifest(path: Path, target_dir: Path) -> dict[str, Any] | Finding:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return Finding(
            "error",
            "MANIFEST_INVALID_JSON",
            f"Manifest is not valid JSON: {exc.msg}.",
            relpath(path, target_dir),
        )
    if not isinstance(data, dict):
        return Finding(
            "error",
            "MANIFEST_INVALID_SHAPE",
            "Manifest root must be a JSON object.",
            relpath(path, target_dir),
        )
    return data


def _validate_manifest(
    manifest: dict[str, Any],
    manifest_path: Path,
    target_dir: Path,
) -> list[Finding]:
    findings: list[Finding] = []
    nodes = _dict_value(manifest, "nodes")
    sources = _dict_value(manifest, "sources")
    child_map = _dict_value(manifest, "child_map")

    model_nodes = {
        unique_id: node
        for unique_id, node in nodes.items()
        if isinstance(node, dict) and node.get("resource_type") == "model"
    }
    if not model_nodes:
        findings.append(
            Finding(
                "warning",
                "MANIFEST_NO_MODELS",
                "Manifest contains no model nodes.",
                relpath(manifest_path, target_dir),
            )
        )

    for unique_id, node in sorted(model_nodes.items()):
        name = str(node.get("name", unique_id))
        original_file_path = str(node.get("original_file_path") or unique_id)
        if not str(node.get("description", "")).strip():
            findings.append(
                Finding(
                    "error",
                    "MODEL_DESCRIPTION_MISSING",
                    f"Model `{name}` has no description.",
                    original_file_path,
                )
            )
        if not _has_test_child(unique_id, child_map, nodes):
            findings.append(
                Finding(
                    "error",
                    "MODEL_TEST_MISSING",
                    f"Model `{name}` has no schema, data, or unit test child in manifest.",
                    original_file_path,
                )
            )
        if _is_mart_model(name) and not _declares_grain(node):
            findings.append(
                Finding(
                    "error",
                    "MART_GRAIN_MISSING",
                    f"Mart model `{name}` must declare grain in meta.grain or description.",
                    original_file_path,
                )
            )

    for source_id, source in sorted(sources.items()):
        if not isinstance(source, dict):
            continue
        source_name = str(source.get("name", source_id))
        source_path = str(source.get("original_file_path") or source_id)
        freshness = source.get("freshness")
        loaded_at_field = source.get("loaded_at_field")
        if not freshness:
            findings.append(
                Finding(
                    "warning",
                    "SOURCE_FRESHNESS_MISSING",
                    f"Source `{source_name}` has no freshness policy.",
                    source_path,
                )
            )
        if freshness and not loaded_at_field:
            findings.append(
                Finding(
                    "warning",
                    "SOURCE_LOADED_AT_MISSING",
                    f"Source `{source_name}` has freshness but no loaded_at_field.",
                    source_path,
                )
            )

    exposures = _dict_value(manifest, "exposures")
    if not exposures:
        findings.append(
            Finding(
                "info",
                "NO_EXPOSURES",
                "Manifest contains no exposures. Add exposures for dashboards, APIs, "
                "and reverse-ETL.",
                relpath(manifest_path, target_dir),
            )
        )
    return findings


def _dict_value(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def _has_test_child(unique_id: str, child_map: dict[str, Any], nodes: dict[str, Any]) -> bool:
    children = child_map.get(unique_id, [])
    if not isinstance(children, list):
        return False
    for child_id in children:
        if not isinstance(child_id, str):
            continue
        child_node = nodes.get(child_id)
        if not isinstance(child_node, dict):
            if child_id.startswith(("test.", "unit_test.")):
                return True
            continue
        if child_node.get("resource_type") in {"test", "unit_test"}:
            return True
    return False


def _is_mart_model(name: str) -> bool:
    return name.startswith(("dim_", "fct_"))


def _declares_grain(node: dict[str, Any]) -> bool:
    meta = node.get("meta")
    if isinstance(meta, dict) and str(meta.get("grain", "")).strip():
        return True
    description = str(node.get("description", "")).lower()
    return "grain:" in description or "grain is" in description or "one row per" in description
