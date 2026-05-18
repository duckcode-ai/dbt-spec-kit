# Tutorial 1: Initialize a dbt repo

This tutorial adds dbt-spec-kit to an existing dbt project and explains what changed.

## Prerequisites

- Python 3.11 or newer
- An existing dbt project with `dbt_project.yml`
- A clean git branch for the adoption work

## 1. Install the CLI

For tutorials and daily use, install the CLI as a persistent tool:

```bash
uv tool install dbt-spec-kit
dbt-specify --version
```

Use `uvx` only for one-time commands. `uvx` does not install a permanent `dbt-specify` command:

```bash
uvx --from dbt-spec-kit dbt-specify --version
```

If you choose `uvx`, keep the prefix on every dbt-spec-kit command:

```bash
uvx --from dbt-spec-kit dbt-specify doctor
```

## 2. Initialize your dbt project

Run from the dbt project root:

```bash
cd path/to/your-dbt-project
dbt-specify init analytics --warehouse snowflake
```

Choose the warehouse preset that matches your project:

- `snowflake`
- `databricks`
- `trino`
- `bigquery`

## 3. Inspect the generated files

`dbt-specify init` creates:

```text
.dbt-specify/
  agents/
  commands/
  constitution.md
  skills/
  templates/
CLAUDE.md
specs/
```

The source templates live in the dbt-spec-kit repo under `agents/`, `commands/`, `skills/`, and
`templates/`. In your dbt project they are generated under `.dbt-specify/`.

## 4. Run doctor

```bash
dbt-specify doctor
```

Expected result:

- no missing `.dbt-specify/` warning
- no missing `.dbt-specify/agents/` warning
- a model inventory if your repo has `models/`
- a `MANIFEST_MISSING` warning until you run `dbt parse`

## 5. Add project conventions

Open `CLAUDE.md` and fill in real team rules:

```text
- Staging models use source, renamed, typed, final CTEs.
- Mart models declare grain in the YAML description.
- PII masking happens before data reaches marts.
- Do not edit semantic model names without reviewer approval.
```

Keep rules specific. Agents follow concrete conventions better than broad advice.

## 6. Try the first business request

Ask your AI agent:

```text
/dbt.specify Add order status normalization to staging without changing downstream mart grain.
```

The expected output is a new directory under `specs/` with `spec.md`. Review the acceptance criteria
before planning.

## Success criteria

- `dbt-specify doctor` runs from the dbt project root.
- `CLAUDE.md` explains the repo's real conventions.
- `.dbt-specify/agents/` exists in the target dbt repo.
- The first feature request creates a spec before any SQL changes.
