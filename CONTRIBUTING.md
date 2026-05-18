# Contributing to dbt-spec-kit

Thanks for considering a contribution. The most useful contributions are:

1. **A new warehouse preset** (Redshift or any other modern adapter). Follow the structure in `presets/snowflake/` (or `presets/trino/` if your target is more like a federated query engine than a warehouse).
2. **A real-world worked example** from an anonymized dbt project.
3. **A validator improvement** for lifecycle artifacts, dbt manifests, semantic models, or warehouse policies.
4. **A tier-3 skill** for a business domain. See `skills/writing-business-glossary-specs/SKILL.md` for the pattern.
5. **Documentation improvements** that make team onboarding easier.

## Local setup

```bash
git clone https://github.com/duckcode-ai/dbt-spec-kit
cd dbt-spec-kit
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
```

All three must pass before opening a PR.

Use the pull request template and include the smallest reproducible example for behavior changes.

## Release changes

Release PRs must keep `pyproject.toml`, `CHANGELOG.md`, and the Git tag aligned. Publishing is
handled by `.github/workflows/release.yml` through PyPI Trusted Publishing, so maintainers should
not add PyPI API tokens or passwords to GitHub secrets.

See `docs/releasing.md` for the full release runbook.

## How to add a warehouse preset

1. Create `presets/<warehouse>/constitution-additions.md`. Append-only — do not repeal base principles.
2. Create `presets/<warehouse>/plan-additions.md`. Add sections to the plan template for warehouse-specific concerns (clustering, governance, cost monitoring, etc.).
3. Add at least one warehouse-specific skill under `presets/<warehouse>/skills/`.
4. Add `--warehouse <name>` to the CLI's `Click.Choice` in `src/dbt_specify/cli.py`.
5. Add a test case mirroring `test_init_databricks_preset`.

## How to write a tier-3 skill

Tier-3 means **business domain context** — not framework conventions (tier 1, owned by dbt-labs/dbt-agent-skills) and not team conventions (tier 2, owned by each project). Tier-3 captures *what your business actually is* — entity definitions, grain decisions, cross-system identifier resolution.

The pattern:
1. Start with a one-paragraph problem statement (a real situation where this context matters).
2. Provide a structured template the user fills in.
3. Give one fully-worked example.
4. List 3–5 anti-patterns to avoid.

See `skills/writing-business-glossary-specs/SKILL.md` for the reference implementation.

## Coding conventions

- Python 3.11+ with type hints everywhere
- `ruff check src tests` and `mypy src` both green before PR
- Sentence-case headers in markdown, no emoji in templates
- New tests for every behavior change

## License

By contributing, you agree your contributions are licensed under MIT (same as the project).
