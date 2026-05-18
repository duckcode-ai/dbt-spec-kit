"""Click command group for the dbt-specify CLI."""
from __future__ import annotations

from pathlib import Path

import click

from dbt_specify._version import __version__
from dbt_specify.confluence import (
    ConfluenceError,
    make_confluence_client,
    pull_page_to_context,
)
from dbt_specify.confluence import (
    publish_spec_dir as publish_confluence_spec_dir,
)
from dbt_specify.confluence import (
    sync_spec_dir as sync_confluence_spec_dir,
)
from dbt_specify.dbt_artifacts import validate_dbt_project
from dbt_specify.doctor import doctor_project
from dbt_specify.init import SUPPORTED_WAREHOUSES, init_project
from dbt_specify.jira import (
    JiraError,
    attach_artifacts,
    create_subtasks_from_tasks,
    make_jira_client,
    pull_issue_to_spec,
    sync_spec_dir,
)
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
    type=click.Choice(SUPPORTED_WAREHOUSES, case_sensitive=False),
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


@main.group()
def jira() -> None:
    """Read from and publish dbt-specify artifacts to Jira Cloud."""


@jira.command("pull")
@click.argument("issue_key")
@click.option(
    "--target",
    "target_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    help="Target dbt project directory (default: current directory).",
)
@click.option(
    "--slug",
    default=None,
    help="Optional slug for the generated specs/<NNN>-<slug>/ directory.",
)
@click.option("--force", is_flag=True, help="Overwrite existing generated files when present.")
def jira_pull(issue_key: str, target_dir: Path, slug: str | None, force: bool) -> None:
    """Create a local spec draft from a Jira issue."""
    try:
        spec_dir = pull_issue_to_spec(
            client=make_jira_client(),
            issue_key=issue_key,
            target_dir=target_dir.resolve(),
            slug=slug,
            force=force,
        )
    except JiraError as error:
        click.echo(f"error: {error}", err=True)
        raise SystemExit(1) from error

    click.echo(f"created {spec_dir / 'spec.md'}")
    click.echo(f"created {spec_dir / 'jira.yml'}")
    click.echo("next: review the draft spec, then run /dbt.plan after approval")


@jira.command("attach")
@click.argument("issue_key")
@click.option("--spec", "spec_path", type=click.Path(dir_okay=False, path_type=Path))
@click.option("--plan", "plan_path", type=click.Path(dir_okay=False, path_type=Path))
@click.option("--tasks", "tasks_path", type=click.Path(dir_okay=False, path_type=Path))
@click.option(
    "--file",
    "extra_files",
    multiple=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Additional artifact to attach. Can be repeated.",
)
@click.option("--no-comment", is_flag=True, help="Do not add a Jira comment after upload.")
def jira_attach(
    issue_key: str,
    spec_path: Path | None,
    plan_path: Path | None,
    tasks_path: Path | None,
    extra_files: tuple[Path, ...],
    no_comment: bool,
) -> None:
    """Attach approved local artifacts to a Jira issue."""
    files = _artifact_paths(spec_path, plan_path, tasks_path, extra_files)
    try:
        uploaded = attach_artifacts(
            client=make_jira_client(),
            issue_key=issue_key,
            files=files,
            comment=not no_comment,
        )
    except JiraError as error:
        click.echo(f"error: {error}", err=True)
        raise SystemExit(1) from error

    for filename in uploaded:
        click.echo(f"attached {filename} to {issue_key}")


@jira.command("create-tasks")
@click.argument("issue_key")
@click.option(
    "--from",
    "tasks_path",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Path to specs/<NNN>-<slug>/tasks.md.",
)
@click.option(
    "--issue-type",
    "issue_type_name",
    default="Sub-task",
    show_default=True,
    help="Jira issue type to create under the parent issue.",
)
@click.option("--include-done", is_flag=True, help="Also create subtasks for checked tasks.")
@click.option("--dry-run", is_flag=True, help="Print the subtasks that would be created.")
def jira_create_tasks(
    issue_key: str,
    tasks_path: Path,
    issue_type_name: str,
    include_done: bool,
    dry_run: bool,
) -> None:
    """Create Jira subtasks from a dbt-specify tasks.md file."""
    try:
        results = create_subtasks_from_tasks(
            client=make_jira_client(),
            issue_key=issue_key,
            tasks_path=tasks_path.resolve(),
            issue_type_name=issue_type_name,
            include_done=include_done,
            dry_run=dry_run,
        )
    except JiraError as error:
        click.echo(f"error: {error}", err=True)
        raise SystemExit(1) from error

    if not results:
        click.echo("no pending tasks found")
        return
    for result in results:
        if result.created:
            click.echo(f"created {result.key}: {result.summary}")
        elif result.key:
            click.echo(f"skipped existing {result.key}: {result.summary}")
        else:
            click.echo(f"would create: {result.summary}")


@jira.command("sync")
@click.argument("issue_key")
@click.option(
    "--spec-dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Path to specs/<NNN>-<slug>/.",
)
@click.option(
    "--issue-type",
    "issue_type_name",
    default="Sub-task",
    show_default=True,
    help="Jira issue type to create under the parent issue.",
)
@click.option("--dry-run", is_flag=True, help="Print task sync actions without writing to Jira.")
def jira_sync(issue_key: str, spec_dir: Path, issue_type_name: str, dry_run: bool) -> None:
    """Attach spec/plan and create Jira subtasks for a spec directory."""
    try:
        uploaded, subtasks = sync_spec_dir(
            client=make_jira_client(),
            issue_key=issue_key,
            spec_dir=spec_dir.resolve(),
            issue_type_name=issue_type_name,
            dry_run=dry_run,
        )
    except JiraError as error:
        click.echo(f"error: {error}", err=True)
        raise SystemExit(1) from error

    for filename in uploaded:
        click.echo(f"attached {filename} to {issue_key}")
    for result in subtasks:
        if result.created:
            click.echo(f"created {result.key}: {result.summary}")
        elif result.key:
            click.echo(f"skipped existing {result.key}: {result.summary}")
        else:
            click.echo(f"would create: {result.summary}")
    if not uploaded and not subtasks:
        click.echo("nothing to sync")


@main.group()
def confluence() -> None:
    """Read from and publish dbt-specify context to Confluence Cloud."""


@confluence.command("pull-page")
@click.argument("page_id")
@click.option(
    "--to",
    "output_path",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Local markdown file to write, usually specs/<NNN>/context/<name>.md.",
)
@click.option(
    "--spec-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Optional spec directory whose confluence.yml should record this source page.",
)
def confluence_pull_page(page_id: str, output_path: Path, spec_dir: Path | None) -> None:
    """Pull a Confluence page into local markdown context."""
    try:
        page = pull_page_to_context(
            client=make_confluence_client(),
            page_id=page_id,
            output_path=output_path.resolve(),
            spec_dir=spec_dir.resolve() if spec_dir else None,
        )
    except ConfluenceError as error:
        click.echo(f"error: {error}", err=True)
        raise SystemExit(1) from error

    click.echo(f"pulled {page.title} ({page.page_id})")
    click.echo(f"wrote {output_path}")


@confluence.command("publish")
@click.option(
    "--spec-dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Path to specs/<NNN>-<slug>/.",
)
@click.option("--space-key", default=None, help="Confluence space key for new pages.")
@click.option("--space-id", default=None, help="Confluence v2 space id for new pages.")
@click.option("--parent-id", default=None, help="Optional Confluence parent page id.")
@click.option("--page-id", default=None, help="Existing Confluence page id to update.")
@click.option("--title", default=None, help="Page title. Defaults to dbt-spec-kit: <spec-dir>.")
@click.option("--dry-run", is_flag=True, help="Print the publish action without writing.")
def confluence_publish(
    spec_dir: Path,
    space_key: str | None,
    space_id: str | None,
    parent_id: str | None,
    page_id: str | None,
    title: str | None,
    dry_run: bool,
) -> None:
    """Create or update a Confluence summary page for a spec directory."""
    try:
        page = publish_confluence_spec_dir(
            client=None if dry_run else make_confluence_client(),
            spec_dir=spec_dir.resolve(),
            space_key=space_key,
            space_id=space_id,
            parent_id=parent_id,
            page_id=page_id,
            title=title,
            dry_run=dry_run,
        )
    except ConfluenceError as error:
        click.echo(f"error: {error}", err=True)
        raise SystemExit(1) from error

    action = "would create" if dry_run and page.created else "would update" if dry_run else (
        "created" if page.created else "updated"
    )
    click.echo(f"{action} Confluence page {page.page_id}: {page.title}")
    if page.page_url != "<dry-run>":
        click.echo(page.page_url)


@confluence.command("sync")
@click.option(
    "--spec-dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Path to specs/<NNN>-<slug>/ with confluence.yml.",
)
@click.option("--dry-run", is_flag=True, help="Print the sync action without writing.")
def confluence_sync(spec_dir: Path, dry_run: bool) -> None:
    """Update the Confluence page recorded in specs/<NNN>/confluence.yml."""
    try:
        page = sync_confluence_spec_dir(
            client=None if dry_run else make_confluence_client(),
            spec_dir=spec_dir.resolve(),
            dry_run=dry_run,
        )
    except ConfluenceError as error:
        click.echo(f"error: {error}", err=True)
        raise SystemExit(1) from error

    action = "would create" if dry_run and page.created else "would update" if dry_run else (
        "created" if page.created else "updated"
    )
    click.echo(f"{action} Confluence page {page.page_id}: {page.title}")
    if page.page_url != "<dry-run>":
        click.echo(page.page_url)


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


def _artifact_paths(
    spec_path: Path | None,
    plan_path: Path | None,
    tasks_path: Path | None,
    extra_files: tuple[Path, ...],
) -> list[Path]:
    files = [path for path in (spec_path, plan_path, tasks_path) if path is not None]
    files.extend(extra_files)
    return [path.resolve() for path in files]


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
