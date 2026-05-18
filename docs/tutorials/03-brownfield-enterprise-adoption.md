# Tutorial 3: Adopt in a brownfield enterprise repo

Most teams will not start from a clean example project. This tutorial shows how to adopt
dbt-spec-kit in a production dbt repo without rewriting existing models.

## 1. Start with diagnostics

Create a branch and run:

```bash
git switch -c adopt/dbt-spec-kit
dbt-specify doctor
```

Treat doctor output as an adoption checklist. It may warn about missing `.dbt-specify/`, `CLAUDE.md`,
`specs/`, `.dbt-specify/agents/`, or `target/manifest.json`.

## 2. Initialize without touching models

```bash
dbt-specify init analytics --warehouse snowflake
```

This should add methodology files, not change production SQL.

If your repo already has `CLAUDE.md`, merge the generated `CLAUDE.md.dbt-specify-suggested` content
manually.

## 3. Capture real project conventions

Use the generated skill:

```text
Use .dbt-specify/skills/capturing-project-conventions/SKILL.md to inspect this repo and propose
rules for CLAUDE.md. Do not edit dbt models.
```

Good conventions include:

- model layer naming
- CTE structure
- source freshness expectations
- test requirements by layer
- owner and tag requirements
- grants, masking, and contract rules

Avoid turning one old model into a global standard without checking current patterns.

## 4. Pick one pilot feature

Choose new work with clear business value and limited file scope. Avoid starting with a migration,
large refactor, or cross-domain Mesh change.

Example request:

```text
/dbt.specify Add a finance-approved net revenue field to the orders mart while preserving existing
order grain and downstream metric names.
```

## 5. Use warning-first CI

At first, attach a report to PRs without blocking merges:

```bash
dbt-specify validate project
dbt parse
dbt-specify validate dbt --manifest target/manifest.json
dbt-specify report --format markdown > dbt-specify-report.md
```

After the team trusts the rules, add a required CI step:

```bash
dbt-specify ci --manifest target/manifest.json
```

## 6. Expand after the pilot

After the first two or three PRs, update:

- `CLAUDE.md` with recurring review feedback
- `.dbt-specify/skills/` with reusable business or governance checks
- warehouse guide additions for team-specific cost rules
- CI requirements for the evidence reviewers expect

## Success criteria

- Existing production models are not rewritten during adoption.
- The first pilot PR has spec, plan, tasks, and report evidence.
- Reviewers can see which AC each model change satisfies.
- CI starts in warning mode before it becomes a merge gate.
