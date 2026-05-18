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


def _markdown_links(text: str) -> list[str]:
    return re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)


def _is_external_or_anchor(link: str) -> bool:
    return link.startswith(("http://", "https://", "mailto:", "#"))
