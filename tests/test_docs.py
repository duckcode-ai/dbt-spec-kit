"""Tests for OSS documentation structure."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_local_links_exist() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text()
    for link in _markdown_links(text):
        if _is_external_or_anchor(link):
            continue
        target = link.split("#", 1)[0]
        if not target:
            continue
        assert (ROOT / target).exists(), f"README link target does not exist: {link}"


def test_jaffle_shop_walkthrough_has_required_commands() -> None:
    text = (ROOT / "docs" / "jaffle-shop-ai-sdlc-walkthrough.md").read_text()
    required_commands = [
        "dbt-specify doctor",
        "dbt-specify init",
        "dbt-specify validate project",
        "dbt parse",
        "dbt-specify validate dbt",
        "dbt-specify report",
    ]
    for command in required_commands:
        assert command in text


def test_implement_all_command_is_documented() -> None:
    command = (ROOT / "commands" / "dbt.implement-all.md").read_text()
    assert "execute approved pending tasks" in command
    assert "Commit using the message format" in command
    assert "Stop immediately" in command
    assert "Never auto-merge" in command

    readme = (ROOT / "README.md").read_text()
    claude_template = (ROOT / "templates" / "CLAUDE.md.template").read_text()
    methodology = (ROOT / "docs" / "methodology.md").read_text()
    assert "/dbt.implement-all" in readme
    assert "/dbt.implement-all" in claude_template
    assert "/dbt.implement-all" in methodology


def test_launch_ready_oss_files_exist() -> None:
    required_paths = [
        "SECURITY.md",
        "SUPPORT.md",
        "ROADMAP.md",
        ".github/pull_request_template.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/workflows/release.yml",
        "docs/releasing.md",
    ]
    for relative_path in required_paths:
        assert (ROOT / relative_path).exists(), f"Missing OSS file: {relative_path}"


def test_release_workflow_uses_trusted_publishing() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text()
    assert "pypa/gh-action-pypi-publish@release/v1" in workflow
    assert "id-token: write" in workflow
    assert "name: pypi" in workflow
    assert "python -m build --sdist --wheel" in workflow
    assert "python -m twine check dist/*" in workflow


def test_skills_and_sub_agents_doc_covers_composition() -> None:
    text = (ROOT / "docs" / "skills-and-sub-agents.md").read_text()
    assert "dbt-labs/dbt-agent-skills" in text
    assert "Do not vendor dbt Labs skills" in text
    assert "not slash commands" in text
    assert "/plugin marketplace add dbt-labs/dbt-agent-skills" in text
    assert "/plugin install dbt@dbt-agent-marketplace" in text
    assert "npx skills add dbt-labs/dbt-agent-skills" in text
    assert "tessl install dbt-labs/dbt-agent-skills" in text
    assert "using-dbt-for-analytics-engineering" in text
    assert "adding-dbt-unit-test" in text
    assert "building-dbt-semantic-layer" in text
    assert "working-with-dbt-mesh" in text
    assert "running-dbt-commands" in text
    assert "fetching-dbt-docs" in text
    for role in (
        "spec-steward",
        "dbt-architect",
        "warehouse-optimizer",
        "implementation-agent",
        "governance-reviewer",
        "review-agent",
    ):
        assert role in text


def test_warehouse_guides_exist_for_supported_presets() -> None:
    from dbt_specify.init import SUPPORTED_WAREHOUSES

    readme = (ROOT / "README.md").read_text()
    getting_started = (ROOT / "docs" / "getting-started.md").read_text()
    for warehouse in SUPPORTED_WAREHOUSES:
        guide = ROOT / "docs" / "warehouse-guides" / f"{warehouse}.md"
        assert guide.exists(), f"Missing warehouse guide: {guide.relative_to(ROOT)}"
        assert f"--warehouse {warehouse}" in guide.read_text()
        assert warehouse in readme
        assert warehouse in getting_started


def test_tutorials_cover_enterprise_onboarding_path() -> None:
    tutorials_dir = ROOT / "docs" / "tutorials"
    required_paths = [
        tutorials_dir / "README.md",
        tutorials_dir / "01-initialize-a-dbt-repo.md",
        tutorials_dir / "02-jaffle-shop-change.md",
        tutorials_dir / "03-brownfield-enterprise-adoption.md",
        tutorials_dir / "04-skills-and-sub-agent-handoffs.md",
    ]
    for path in required_paths:
        assert path.exists(), f"Missing tutorial: {path.relative_to(ROOT)}"
        _assert_local_links_exist(path)

    index = (tutorials_dir / "README.md").read_text()
    assert "Initialize a dbt repo" in index
    assert "Ship a jaffle-shop change" in index
    assert "Adopt in a brownfield enterprise repo" in index
    assert "Run skills and sub-agent handoffs" in index

    handoffs = (tutorials_dir / "04-skills-and-sub-agent-handoffs.md").read_text()
    assert "dbt Labs skills" in handoffs
    assert ".dbt-specify/agents/" in handoffs
    assert "Human approval remains the merge gate" in handoffs


def _markdown_links(text: str) -> list[str]:
    return re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)


def _is_external_or_anchor(link: str) -> bool:
    return link.startswith(("http://", "https://", "mailto:", "#"))


def _assert_local_links_exist(path: Path) -> None:
    text = path.read_text()
    for link in _markdown_links(text):
        if _is_external_or_anchor(link):
            continue
        target = link.split("#", 1)[0]
        if not target:
            continue
        assert (path.parent / target).resolve().exists(), (
            f"{path.relative_to(ROOT)} link target does not exist: {link}"
        )
