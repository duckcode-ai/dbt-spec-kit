"""Click command group for the dbt-specify CLI."""
from __future__ import annotations

from pathlib import Path

import click

from dbt_specify._version import __version__
from dbt_specify.init import init_project
from dbt_specify.validate import validate_spec


@click.group()
@click.version_option(__version__, prog_name="dbt-specify")
def main() -> None:
    """dbt-specify — spec-driven development for dbt projects."""


@main.command()
@click.argument("project_name")
@click.option(
    "--warehouse",
    type=click.Choice(["snowflake", "databricks", "trino"], case_sensitive=False),
    required=True,
    help="Warehouse preset to install alongside the base constitution.",
)
@click.option(
    "--target",
    "target_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    help="Target directory (default: current directory).",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite an existing .dbt-specify/ directory.",
)
def init(project_name: str, warehouse: str, target_dir: Path, force: bool) -> None:
    """Initialize dbt-specify in an existing dbt project."""
    init_project(
        project_name=project_name,
        warehouse=warehouse.lower(),
        target_dir=target_dir.resolve(),
        force=force,
    )


@main.command()
@click.argument(
    "spec_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def validate(spec_path: Path) -> None:
    """Validate that a spec.md's Acceptance Criteria are EARS-conformant."""
    exit_code = validate_spec(spec_path.resolve())
    raise SystemExit(exit_code)


@main.command()
def version() -> None:
    """Print the installed version."""
    click.echo(__version__)


if __name__ == "__main__":
    main()
