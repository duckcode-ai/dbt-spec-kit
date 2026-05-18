"""Click command group for the dbt-specify CLI."""
from __future__ import annotations

from pathlib import Path

import click

from dbt_specify._version import __version__
from dbt_specify.dbt_artifacts import validate_dbt_project
from dbt_specify.doctor import doctor_project
from dbt_specify.init import init_project
from dbt_specify.lifecycle import validate_lifecycle
from dbt_specify.reporting import ValidationReport, combine_reports
from dbt_specify.validate import validate_spec


@click.group()
@click.version_option(__version__, prog_name="dbt-specify")
def main() -> None:
    """dbt-specify — spec-driven development for dbt projects."""


@main.command()
@click.argument("project_name")
@click.option(
    "--warehouse",
    type=click.Choice(["snowflake", "databricks", "trino", "bigquery"], case_sensitive=False),
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


@main.command(
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    }
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def validate(args: tuple[str, ...]) -> None:
    """Validate specs, lifecycle artifacts, or dbt project artifacts.

    Usage:
      dbt-specify validate path/to/spec.md
      dbt-specify validate project --target .
      dbt-specify validate dbt --target . --manifest target/manifest.json
    """
    if not args:
        click.echo(
            "Usage:\n"
            "  dbt-specify validate path/to/spec.md\n"
            "  dbt-specify validate project --target .\n"
            "  dbt-specify validate dbt --target . --manifest target/manifest.json"
        )
        raise SystemExit(2)

    subcommand = args[0]
    if subcommand == "project":
        target_dir = _path_option(args[1:], "--target", Path(".")).resolve()
        report = validate_lifecycle(target_dir)
        _echo_report(report, "markdown")
        raise SystemExit(report.exit_code)
    if subcommand == "dbt":
        target_dir = _path_option(args[1:], "--target", Path(".")).resolve()
        manifest_path = _optional_path_option(args[1:], "--manifest")
        report = validate_dbt_project(
            target_dir=target_dir,
            manifest_path=manifest_path.resolve() if manifest_path else None,
        )
        _echo_report(report, "markdown")
        raise SystemExit(report.exit_code)
    if len(args) != 1:
        click.echo(
            "error: expected `validate <spec.md>`, `validate project`, or `validate dbt`",
            err=True,
        )
        raise SystemExit(2)

    spec_path = Path(args[0])
    if not spec_path.exists() or not spec_path.is_file():
        click.echo(f"error: spec file not found: {spec_path}", err=True)
        raise SystemExit(1)
    exit_code = validate_spec(spec_path.resolve())
    raise SystemExit(exit_code)


@main.command()
@click.option(
    "--target",
    "target_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    help="Target dbt project directory (default: current directory).",
)
def doctor(target_dir: Path) -> None:
    """Inspect a brownfield dbt repo for adoption gaps."""
    report = doctor_project(target_dir.resolve())
    _echo_report(report, "markdown")
    raise SystemExit(report.exit_code)


@main.command(name="report")
@click.option(
    "--target",
    "target_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    help="Target dbt project directory (default: current directory).",
)
@click.option(
    "--manifest",
    "manifest_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="Optional dbt manifest path (default: target/manifest.json).",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["markdown", "json"], case_sensitive=False),
    default="markdown",
    help="Output format.",
)
def report(target_dir: Path, manifest_path: Path | None, output_format: str) -> None:
    """Emit CI-ready validation evidence."""
    combined = _combined_validation_report(target_dir.resolve(), manifest_path)
    _echo_report(combined, output_format.lower())
    raise SystemExit(combined.exit_code)


@main.command()
@click.option(
    "--target",
    "target_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    help="Target dbt project directory (default: current directory).",
)
@click.option(
    "--manifest",
    "manifest_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="Optional dbt manifest path (default: target/manifest.json).",
)
def ci(target_dir: Path, manifest_path: Path | None) -> None:
    """Run release-blocking dbt-specify checks for CI."""
    combined = _combined_validation_report(
        target_dir.resolve(),
        manifest_path,
        require_manifest=True,
    )
    _echo_report(combined, "markdown")
    raise SystemExit(combined.exit_code)


@main.command()
def version() -> None:
    """Print the installed version."""
    click.echo(__version__)


def _combined_validation_report(
    target_dir: Path,
    manifest_path: Path | None,
    require_manifest: bool = False,
) -> ValidationReport:
    resolved_manifest = manifest_path.resolve() if manifest_path else None
    return combine_reports(
        "dbt-specify CI report",
        [
            validate_lifecycle(target_dir),
            validate_dbt_project(target_dir, resolved_manifest, require_manifest=require_manifest),
        ],
    )


def _echo_report(report: ValidationReport, output_format: str) -> None:
    if output_format == "json":
        click.echo(report.to_json())
        return
    click.echo(report.to_markdown())


def _path_option(args: tuple[str, ...], flag: str, default: Path) -> Path:
    value = _optional_path_option(args, flag)
    return value or default


def _optional_path_option(args: tuple[str, ...], flag: str) -> Path | None:
    for index, arg in enumerate(args):
        if arg == flag:
            try:
                return Path(args[index + 1])
            except IndexError:
                click.echo(f"error: {flag} requires a path", err=True)
                raise SystemExit(2) from None
        prefix = f"{flag}="
        if arg.startswith(prefix):
            return Path(arg.removeprefix(prefix))
    return None


if __name__ == "__main__":
    main()
