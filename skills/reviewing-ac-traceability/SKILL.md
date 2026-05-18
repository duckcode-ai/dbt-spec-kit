---
name: reviewing-ac-traceability
description: Use when checking that a dbt change traces from acceptance criteria to plan, tasks, code, tests, and review evidence.
---

# Reviewing AC traceability

## When to use this skill

Use this before implementation, before review, and before attaching PR evidence.

## Review routine

1. List every AC id from `spec.md`.
2. Confirm each AC id appears in `plan.md`.
3. Confirm each AC id appears in at least one task in `tasks.md`.
4. Confirm each implemented file maps back to a planned task.
5. Confirm each AC has validation evidence: dbt test, dbt parse, manifest check, SQL review, or
   explicit human review.
6. Block review if code exists for an AC that is not in the approved spec.

## Common failures

- A task says it supports an AC but no test or review evidence exists.
- A model changed because it was nearby, not because the approved plan listed it.
- A reviewer approves functionality without checking the AC id list.

## Output

Return a table:

| AC id | Plan reference | Task reference | Evidence | Status |
|---|---|---|---|---|
