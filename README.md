# dbt-spec-kit

> Spec-driven development for dbt — with warehouse-specific presets for Snowflake, Databricks, and Trino.

Modeled on [github/spec-kit](https://github.com/github/spec-kit). Composes with [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills). Works with Claude Code, Cursor, GitHub Copilot, Gemini CLI, Cline, and any agent that reads markdown context.

## Why this exists

AI coding agents are powerful but vague. "Build a customer mart" gets you wildly different output depending on agent context. dbt-spec-kit fixes that by making **specs the source of truth**: written once, agent-readable, warehouse-aware.

Four phases, one human checkpoint per phase, never auto-merge.

```
Specify  →  Plan  →  Tasks  →  Implement
   ↑                                |
   └──────────  retro  ←────────────┘
```

## Install

Requires Python 3.11+. Recommended via [uv](https://docs.astral.sh/uv/):

```bash
uvx --from git+https://github.com/duckcode-ai/dbt-spec-kit.git dbt-specify init my-project --warehouse snowflake
```

Or persistent install:

```bash
uv tool install dbt-spec-kit --from git+https://github.com/duckcode-ai/dbt-spec-kit.git
dbt-specify init my-project --warehouse snowflake
```

## What you get

Running `init` in your existing dbt project creates:

- `.dbt-specify/constitution.md` — the project's non-negotiable principles (base + warehouse-specific additions)
- `.dbt-specify/templates/` — spec, plan, tasks, retro templates
- `.dbt-specify/skills/` — tier-2 and tier-3 skills for writing specs
- `.dbt-specify/commands/` — slash-command prompts (`/dbt.specify`, `/dbt.plan`, `/dbt.tasks`, `/dbt.implement`)
- `CLAUDE.md` — references the constitution, defers tier-1 questions to `dbt-labs/dbt-agent-skills`
- `specs/` — empty directory for your first spec

## The three positioning pillars

| Pillar | What we ship |
|---|---|
| Methodology layer | Constitution + four-phase templates + CLI |
| Warehouse presets | Snowflake (clustering, warehouse sizing, query tags, masking), Databricks (Liquid Clustering, Photon, Unity Catalog), and Trino (federation patterns, catalog discipline, connector pushdown) |
| Tier-3 skills | The one nobody else ships — writing business glossary and entity-resolution specs |

## What this is not

- **Not a replacement** for `dbt-labs/dbt-agent-skills`. Install both. They compose.
- **Not an IDE.** Markdown templates and a thin CLI. Bring your own agent.
- **Not opinionated about agents.** Works with anything that reads markdown context.

## Worked example

See [`examples/jaffle-shop-staging-overhaul/`](examples/jaffle-shop-staging-overhaul/) for a complete spec → plan → tasks → implementation trace.

## Docs

- [Getting started](docs/getting-started.md) — install + your first spec in 5 minutes
- [Methodology](docs/methodology.md) — the four-phase loop in depth
- [EARS cheatsheet](docs/ears-cheatsheet.md) — the five testable spec patterns with dbt examples
- [Snowflake guide](docs/warehouse-guides/snowflake.md)
- [Databricks guide](docs/warehouse-guides/databricks.md)
- [Trino guide](docs/warehouse-guides/trino.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The most useful contributions today: a BigQuery preset, more tier-3 skills, real-world worked examples from your project.

## License

MIT.
