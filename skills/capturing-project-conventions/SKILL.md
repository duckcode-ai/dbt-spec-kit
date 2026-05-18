---
name: capturing-project-conventions
description: Use when turning an existing dbt repository's naming, layering, testing, materialization, and review patterns into reusable agent guidance.
---

# Capturing project conventions

## When to use this skill

Use this during brownfield onboarding, retros, and after reviewers repeatedly correct the same
agent behavior.

## Discovery routine

1. Inspect `dbt_project.yml` for model paths, materializations, quoting, dispatch, and vars.
2. Sample staging, intermediate, mart, source, exposure, and metric files.
3. Record naming conventions, CTE structure, test patterns, contracts, tags, owners, and grants.
4. Separate hard rules from examples. Hard rules belong in `CLAUDE.md` or the constitution.
5. Turn repeated review feedback into a focused skill under `.dbt-specify/skills/`.

## Output

Return:

- Rules to add to `CLAUDE.md`.
- Candidate skills to add or update.
- Anti-patterns the agent should avoid.
- Examples from real repo files.

## Common failures

- Treating one old model as the standard without checking newer models.
- Capturing business meaning as a project convention instead of a business glossary spec.
- Making guidance too broad for a skill to trigger reliably.
