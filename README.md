# dbt-spec-kit

> AI SDLC for dbt teams: specs are contracts, agents do bounded implementation, and CI proves the
> work followed the plan.

dbt-spec-kit helps analytics engineering teams use AI coding agents safely inside real dbt projects.
It adds a lightweight spec-driven workflow, warehouse-aware planning templates, agent prompts, and
CI validation to an existing dbt repo.

It is modeled on [GitHub Spec Kit](https://github.com/github/spec-kit), composes with
[dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills), and works with any agent
that reads markdown context, including Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, and
Cline.

## Why teams use it

AI agents are useful, but "build a customer mart" is too vague for enterprise dbt work. A safe dbt
change needs grain, source contracts, tests, semantic-layer impact, downstream consumers, warehouse
cost decisions, and human approval points.

dbt-spec-kit turns that into a repeatable loop:

```text
Idea -> spec.md -> plan.md -> tasks.md -> dbt changes -> CI report -> review
```

The default is controlled autonomy. Agents can draft and implement, but humans approve the spec, the
plan, and the final diff.

## Try it with jaffle-shop

The fastest way to understand the workflow is to apply it to the upstream
[dbt-labs/jaffle-shop](https://github.com/dbt-labs/jaffle-shop) project.

```bash
git clone https://github.com/dbt-labs/jaffle-shop.git
cd jaffle-shop

uvx --from dbt-spec-kit dbt-specify init jaffle-shop --warehouse bigquery

dbt-specify doctor
```

Then use your AI agent:

```text
/dbt.specify Add a customer segmentation field to the customers mart without breaking existing metrics.
/dbt.plan
/dbt.tasks
/dbt.implement
/dbt.review
```

See the full walkthrough: [Jaffle-shop AI SDLC walkthrough](docs/jaffle-shop-ai-sdlc-walkthrough.md).

## Install

Requires Python 3.11+. Recommended via [uv](https://docs.astral.sh/uv/).

```bash
uvx --from dbt-spec-kit dbt-specify init my-project --warehouse snowflake
```

From GitHub source for development builds:

```bash
uvx --from git+https://github.com/duckcode-ai/dbt-spec-kit.git \
  dbt-specify init my-project --warehouse snowflake
```

Persistent install:

```bash
uv tool install dbt-spec-kit
dbt-specify --version
```

Supported warehouse presets: `snowflake`, `databricks`, `trino`, `bigquery`, `redshift`,
`postgres`, `sqlserver`, `azure-sql`, `mysql`, `duckdb`, `motherduck`, and `athena`.

## What init adds

Running `dbt-specify init` in an existing dbt project creates:

- `.dbt-specify/constitution.md` for project principles and warehouse guardrails
- `.dbt-specify/templates/` for spec, plan, tasks, retro, and CI templates
- `.dbt-specify/skills/` for spec-writing guidance
- `.dbt-specify/commands/` for agent prompts
- `.dbt-specify/agents/` for sub-agent role and handoff templates
- `CLAUDE.md` or `CLAUDE.md.dbt-specify-suggested`
- `specs/` for feature-level SDLC artifacts

## Skills vs sub-agents

Skills are reusable knowledge. They teach an agent how to do a category of work better, such as
writing mart specs with grain, checking PII access rules, or using dbt Labs guidance for unit tests.

Sub-agents are bounded workers. Their templates define the mission, required context, allowed edit
paths, forbidden files, and output contract for a specific handoff.

Use dbt Labs skills for dbt framework mechanics. Use dbt-spec-kit skills and sub-agent roles for the
enterprise delivery workflow around specs, plans, governance, warehouse guardrails, and CI evidence.

The agent commands are:

- `/dbt.specify` drafts the requirement.
- `/dbt.plan` creates a file-by-file implementation contract.
- `/dbt.tasks` decomposes the approved plan into small tasks.
- `/dbt.implement` executes one task at a time.
- `/dbt.implement-all` executes approved pending tasks sequentially, stopping on validation or scope failures.
- `/dbt.analyze` checks traceability before implementation.
- `/dbt.review` reviews the final diff against the approved plan.

## CI trust boundary

Use these checks locally or in CI:

```bash
dbt-specify validate project
dbt parse
dbt-specify validate dbt --manifest target/manifest.json
dbt-specify report --format markdown
```

Use `dbt-specify ci` when the lifecycle and dbt artifact checks should block a PR.

## Who this is for

- Analytics engineers who want AI help without losing dbt conventions.
- Data platform leads standardizing AI-assisted delivery across teams.
- dbt consultants who need a repeatable client onboarding method.
- OSS contributors building warehouse presets, validators, examples, and skills.

## Docs

- [Getting started](docs/getting-started.md)
- [Tutorials](docs/tutorials/README.md)
- [Jaffle-shop AI SDLC walkthrough](docs/jaffle-shop-ai-sdlc-walkthrough.md)
- [Team onboarding playbook](docs/team-onboarding-playbook.md)
- [Methodology](docs/methodology.md)
- [Skills and sub-agents](docs/skills-and-sub-agents.md)
- [Enterprise CI](docs/enterprise-ci.md)
- [Brownfield onboarding](docs/brownfield-onboarding.md)
- [EARS cheatsheet](docs/ears-cheatsheet.md)
- [Releasing to PyPI](docs/releasing.md)
- [Snowflake guide](docs/warehouse-guides/snowflake.md)
- [Databricks guide](docs/warehouse-guides/databricks.md)
- [Trino guide](docs/warehouse-guides/trino.md)
- [BigQuery guide](docs/warehouse-guides/bigquery.md)
- [Redshift guide](docs/warehouse-guides/redshift.md)
- [Postgres guide](docs/warehouse-guides/postgres.md)
- [SQL Server guide](docs/warehouse-guides/sqlserver.md)
- [Azure SQL guide](docs/warehouse-guides/azure-sql.md)
- [MySQL guide](docs/warehouse-guides/mysql.md)
- [DuckDB guide](docs/warehouse-guides/duckdb.md)
- [MotherDuck guide](docs/warehouse-guides/motherduck.md)
- [Athena guide](docs/warehouse-guides/athena.md)

## OSS project

- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Support](SUPPORT.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

## What this is not

- Not a replacement for dbt or dbt Cloud.
- Not a replacement for `dbt-labs/dbt-agent-skills`.
- Not an IDE or hosted service.
- Not full autonomy or auto-merge.

## License

MIT.
