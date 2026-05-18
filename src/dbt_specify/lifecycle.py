"""Validate dbt-spec-kit lifecycle artifacts."""
from __future__ import annotations

import re
from pathlib import Path

from dbt_specify.ears import classify_ears
from dbt_specify.reporting import Finding, ValidationReport
from dbt_specify.validate import _extract_ac_lines

_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(?P<status>.+?)\s*$", re.IGNORECASE | re.MULTILINE)
_AC_ID_RE = re.compile(r"\bAC(?P<num>\d+[A-Za-z]?)\b")
_REQUIRED_PLAN_SECTIONS = (
    "## Architecture",
    "## Files to add",
    "## Files to modify",
    "## Files to delete",
    "## Tests",
    "## Downstream impact",
)


def validate_lifecycle(target_dir: Path) -> ValidationReport:
    """Validate spec -> plan -> tasks traceability for a dbt project."""
    findings: list[Finding] = []
    specs_dir = target_dir / "specs"
    if not specs_dir.exists():
        return ValidationReport(
            "dbt-specify project validation",
            (
                Finding(
                    "warning",
                    "PROJECT_NO_SPECS_DIR",
                    "No specs/ directory found. Run `dbt-specify init` before using the "
                    "enterprise workflow.",
                    relpath(specs_dir, target_dir),
                ),
            ),
        )

    spec_dirs = sorted(path for path in specs_dir.iterdir() if path.is_dir())
    if not spec_dirs:
        findings.append(
            Finding(
                "warning",
                "PROJECT_NO_SPECS",
                "specs/ exists but contains no feature specs yet.",
                relpath(specs_dir, target_dir),
            )
        )

    for spec_dir in spec_dirs:
        findings.extend(_validate_spec_dir(spec_dir, target_dir))

    return ValidationReport("dbt-specify project validation", tuple(findings))


def _validate_spec_dir(spec_dir: Path, target_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    spec_path = spec_dir / "spec.md"
    plan_path = spec_dir / "plan.md"
    tasks_path = spec_dir / "tasks.md"

    if not spec_path.exists():
        return [
            Finding(
                "error",
                "SPEC_MISSING",
                "Spec directory is missing spec.md.",
                relpath(spec_path, target_dir),
            )
        ]

    spec_text = spec_path.read_text()
    ac_lines = _extract_ac_lines(spec_text)
    ac_ids = _extract_referenced_ac_ids(spec_text)
    spec_status = _read_status(spec_text)

    if not ac_lines:
        findings.append(
            Finding(
                "error",
                "SPEC_NO_ACCEPTANCE_CRITERIA",
                "spec.md has no Acceptance Criteria section.",
                relpath(spec_path, target_dir),
            )
        )
    for line_no, line in ac_lines:
        if classify_ears(line) is None:
            findings.append(
                Finding(
                    "error",
                    "SPEC_NON_EARS_AC",
                    f"Acceptance criterion on line {line_no} is not EARS-formatted.",
                    relpath(spec_path, target_dir),
                )
            )
    if ac_lines and not ac_ids:
        findings.append(
            Finding(
                "warning",
                "SPEC_UNLABELED_ACS",
                "Acceptance criteria should use stable AC ids such as AC1, AC2, AC3.",
                relpath(spec_path, target_dir),
            )
        )

    if plan_path.exists():
        findings.extend(_validate_plan(plan_path, spec_status, ac_ids, target_dir))
    if tasks_path.exists():
        findings.extend(_validate_tasks(tasks_path, plan_path, ac_ids, target_dir))

    return findings


def _validate_plan(
    plan_path: Path,
    spec_status: str | None,
    ac_ids: set[str],
    target_dir: Path,
) -> list[Finding]:
    findings: list[Finding] = []
    plan_text = plan_path.read_text()
    plan_status = _read_status(plan_text)

    if not _is_approved(spec_status):
        findings.append(
            Finding(
                "error",
                "PLAN_BEFORE_SPEC_APPROVAL",
                "plan.md exists before spec.md is marked approved or shipped.",
                relpath(plan_path, target_dir),
            )
        )
    if plan_status is None:
        findings.append(
            Finding(
                "error",
                "PLAN_STATUS_MISSING",
                "plan.md must include a `Status:` line.",
                relpath(plan_path, target_dir),
            )
        )
    for section in _REQUIRED_PLAN_SECTIONS:
        if section.lower() not in plan_text.lower():
            findings.append(
                Finding(
                    "error",
                    "PLAN_SECTION_MISSING",
                    f"plan.md is missing required section `{section}`.",
                    relpath(plan_path, target_dir),
                )
            )

    findings.extend(_validate_ac_traceability(ac_ids, plan_text, plan_path, target_dir, "plan.md"))
    return findings


def _validate_tasks(
    tasks_path: Path,
    plan_path: Path,
    ac_ids: set[str],
    target_dir: Path,
) -> list[Finding]:
    findings: list[Finding] = []
    tasks_text = tasks_path.read_text()
    plan_text = plan_path.read_text() if plan_path.exists() else ""
    plan_status = _read_status(plan_text)

    if not plan_path.exists():
        findings.append(
            Finding(
                "error",
                "TASKS_WITHOUT_PLAN",
                "tasks.md exists before plan.md.",
                relpath(tasks_path, target_dir),
            )
        )
    elif not _is_approved(plan_status):
        findings.append(
            Finding(
                "error",
                "TASKS_BEFORE_PLAN_APPROVAL",
                "tasks.md exists before plan.md is marked approved.",
                relpath(tasks_path, target_dir),
            )
        )

    if "## Task list" not in tasks_text:
        findings.append(
            Finding(
                "error",
                "TASKS_SECTION_MISSING",
                "tasks.md must include a `## Task list` section.",
                relpath(tasks_path, target_dir),
            )
        )
    findings.extend(
        _validate_ac_traceability(ac_ids, tasks_text, tasks_path, target_dir, "tasks.md")
    )
    return findings


def _validate_ac_traceability(
    ac_ids: set[str],
    text: str,
    path: Path,
    target_dir: Path,
    artifact_name: str,
) -> list[Finding]:
    if not ac_ids:
        return []
    referenced = _extract_referenced_ac_ids(text)
    findings: list[Finding] = []
    for ac_id in sorted(ac_ids):
        if ac_id not in referenced:
            findings.append(
                Finding(
                    "error",
                    "AC_NOT_TRACED",
                    f"{artifact_name} does not reference {ac_id}.",
                    relpath(path, target_dir),
                )
            )
    return findings


def _read_status(text: str) -> str | None:
    match = _STATUS_RE.search(text)
    if match is None:
        return None
    return match.group("status").strip().lower()


def _is_approved(status: str | None) -> bool:
    return status is not None and any(word in status for word in ("approved", "shipped", "done"))


def _extract_referenced_ac_ids(text: str) -> set[str]:
    return {f"AC{match.group('num')}" for match in _AC_ID_RE.finditer(text)}


def relpath(path: Path, base: Path) -> str:
    """Return a stable display path relative to the target project when possible."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)
