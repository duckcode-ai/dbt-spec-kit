# Getting started with dbt-spec-kit

Five-minute install plus your first spec-driven dbt workflow.

## Prerequisites

- Python 3.11+
- An existing dbt project (we don't generate dbt projects, we add spec-driven structure to them)
- An AI coding agent that reads markdown context (Claude Code, Cursor, GitHub Copilot, Gemini CLI, Cline, etc.)

## Install

The recommended path uses `uv` for isolated tool installation:

```bash
# install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# install dbt-specify as a tool
uv tool install dbt-spec-kit --from git+https://github.com/duckcode-ai/dbt-spec-kit.git
```

Verify:

```bash
dbt-specify --version
```

## Initialize in your dbt project

```bash
cd path/to/your-dbt-project
dbt-specify init my-project --warehouse snowflake
```

This creates:
- `.dbt-specify/constitution.md` — the project's non-negotiable principles
- `.dbt-specify/templates/` — spec, plan, tasks, retro
- `.dbt-specify/skills/` — tier-2 and tier-3 spec-writing skills
- `.dbt-specify/commands/` — slash-command prompts
- `CLAUDE.md` — the agent orientation file (or `CLAUDE.md.dbt-specify-suggested` if you already have one)
- `specs/` — empty directory for your first spec

Supported warehouse presets: `snowflake`, `databricks`, `trino`, and `bigquery`.

## Compose with dbt-labs/dbt-agent-skills

Install dbt-agent-skills separately to cover the "how does dbt work" tier:

```bash
# Vercel Skills CLI path
npx skills add dbt-labs/dbt-agent-skills

# or via Tessl
tessl install dbt-labs/dbt-agent-skills
```

CLAUDE.md from `dbt-specify init` already defers tier-1 questions to that collection.

## Your first spec

In your AI agent, invoke `/dbt.specify <description of the feature>`. The agent will:

1. Read the constitution
2. Pick the right spec-writing skill (staging, mart, or business glossary)
3. Draft `specs/001-<slug>/spec.md`
4. Tell you to review

Once you approve, run `/dbt.plan` to get a plan, then `/dbt.tasks` to break it down, then `/dbt.implement` to execute one task at a time.

Validate your spec is EARS-conformant:

```bash
dbt-specify validate specs/001-<slug>/spec.md
```

Before implementation or review, validate the lifecycle and dbt artifacts:

```bash
dbt-specify validate project
dbt parse
dbt-specify validate dbt --manifest target/manifest.json
dbt-specify report --format markdown
```

For an existing dbt repo, start with:

```bash
dbt-specify doctor
```

## Next steps

- Try the [jaffle-shop AI SDLC walkthrough](jaffle-shop-ai-sdlc-walkthrough.md) to see the process on a real dbt Labs project.
- Use the [team onboarding playbook](team-onboarding-playbook.md) when presenting the workflow to an analytics engineering team.
- Read [methodology.md](methodology.md) for the full four-phase loop.
- Read [warehouse-guides/snowflake.md](warehouse-guides/snowflake.md) or [databricks.md](warehouse-guides/databricks.md) for your warehouse's preset.
- See [`examples/jaffle-shop-staging-overhaul/`](../examples/jaffle-shop-staging-overhaul/) for a complete worked example.
