"""Implementation of `dbt-specify init`."""
from __future__ import annotations

import shutil
from pathlib import Path

import click

from dbt_specify.templates_loader import asset_dir

# Filter junk that may live in the source tree during editable installs
# (macOS Finder leftovers, pyc caches, etc.) so user-visible output stays clean.
_IGNORE_JUNK = shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", ".gitkeep")


def init_project(
    project_name: str,
    warehouse: str,
    target_dir: Path,
    force: bool,
) -> None:
    """Initialize a .dbt-specify/ directory in an existing dbt project.

    Args:
        project_name: Human-readable name for the project (logged, not enforced).
        warehouse: One of "snowflake", "databricks", "trino", or "bigquery".
        target_dir: Where to write the .dbt-specify/ directory.
        force: If True, overwrite existing .dbt-specify/.

    Raises:
        SystemExit: On any precondition failure.
    """
    if warehouse not in {"snowflake", "databricks", "trino", "bigquery"}:
        click.echo(f"error: unknown warehouse '{warehouse}'", err=True)
        raise SystemExit(2)

    dbt_project_yml = target_dir / "dbt_project.yml"
    if not dbt_project_yml.exists():
        click.echo(
            f"error: no dbt_project.yml found at {target_dir}.\n"
            f"  dbt-specify init must be run inside an existing dbt project.\n"
            f"  see docs/getting-started.md for help.",
            err=True,
        )
        raise SystemExit(1)

    specify_dir = target_dir / ".dbt-specify"
    if specify_dir.exists():
        if not force:
            click.echo(
                f"error: {specify_dir} already exists.\n"
                f"  re-run with --force to overwrite.",
                err=True,
            )
            raise SystemExit(1)
        shutil.rmtree(specify_dir)

    specify_dir.mkdir(parents=True, exist_ok=False)

    # 1. Copy base constitution
    _copy_file(
        src=asset_dir("memory") / "constitution.md",
        dst=specify_dir / "constitution.md",
    )

    # 2. Append warehouse-specific additions to the constitution
    additions = (asset_dir("presets") / warehouse / "constitution-additions.md").read_text()
    base_constitution = (specify_dir / "constitution.md").read_text()
    (specify_dir / "constitution.md").write_text(
        base_constitution
        + f"\n\n<!-- BEGIN {warehouse.upper()} ADDITIONS -->\n\n"
        + additions
        + f"\n\n<!-- END {warehouse.upper()} ADDITIONS -->\n"
    )

    # 3. Copy templates
    templates_dst = specify_dir / "templates"
    shutil.copytree(asset_dir("templates"), templates_dst, ignore=_IGNORE_JUNK)

    # 4. Append warehouse-specific plan additions to plan-template
    plan_additions = (asset_dir("presets") / warehouse / "plan-additions.md").read_text()
    plan_path = templates_dst / "plan-template.md"
    plan_path.write_text(
        plan_path.read_text()
        + f"\n\n<!-- BEGIN {warehouse.upper()} PLAN ADDITIONS -->\n\n"
        + plan_additions
        + f"\n\n<!-- END {warehouse.upper()} PLAN ADDITIONS -->\n"
    )

    # 5. Copy skills
    skills_dst = specify_dir / "skills"
    shutil.copytree(asset_dir("skills"), skills_dst, ignore=_IGNORE_JUNK)

    # 6. Copy warehouse-specific skills
    warehouse_skills_src = asset_dir("presets") / warehouse / "skills"
    if warehouse_skills_src.exists():
        for skill_dir in warehouse_skills_src.iterdir():
            if skill_dir.is_dir():
                shutil.copytree(skill_dir, skills_dst / skill_dir.name, ignore=_IGNORE_JUNK)

    # 7. Copy commands
    commands_dst = specify_dir / "commands"
    shutil.copytree(asset_dir("commands"), commands_dst, ignore=_IGNORE_JUNK)

    # 8. Create or suggest CLAUDE.md
    claude_template = (
        (asset_dir("templates") / "CLAUDE.md.template")
        .read_text()
        .replace("{{ project_name }}", project_name)
        .replace("{{ warehouse }}", warehouse)
    )

    claude_target = target_dir / "CLAUDE.md"
    if claude_target.exists():
        suggested = target_dir / "CLAUDE.md.dbt-specify-suggested"
        suggested.write_text(claude_template)
        click.echo(
            f"note: {claude_target.name} already exists.\n"
            f"  wrote a suggested merge to {suggested.name} — review and integrate manually."
        )
    else:
        claude_target.write_text(claude_template)
        click.echo(f"wrote {claude_target.name}")

    # 9. Create empty specs/ directory for the user's first spec
    (target_dir / "specs").mkdir(exist_ok=True)
    (target_dir / "specs" / ".gitkeep").touch()

    click.echo(f"\ndbt-specify initialized in {target_dir}")
    click.echo(f"  warehouse preset: {warehouse}")
    click.echo(
        f"  next: see {target_dir}/.dbt-specify/constitution.md and {target_dir}/CLAUDE.md"
    )


def _copy_file(src: Path, dst: Path) -> None:
    """Copy a single file, creating parent dirs if needed."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
