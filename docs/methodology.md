# Methodology — the four-phase loop, dbt-flavored

## Overview

```
Specify  →  Plan  →  Tasks  →  Implement
   ↑                                |
   └──────────  retro  ←────────────┘
```

Each phase has a **human checkpoint**. No phase skips, no auto-merge.

## Phase 1: Specify

**Input:** a feature description (one sentence or one paragraph).
**Output:** `specs/<NNN>-<slug>/spec.md`.
**Human checkpoint:** the spec is reviewed and marked `Status: approved`.

The spec answers: what problem, who's affected, what's the result, what are the acceptance criteria, what's out of scope, what are the constraints. ACs are EARS-formatted and validatable with `dbt-specify validate`.

If the spec describes a staging model, use the `writing-staging-model-specs` skill. For mart-level work, use `writing-mart-specs-with-grain`. For anything involving entities that span systems, also use `writing-business-glossary-specs`.

## Phase 2: Plan

**Input:** an approved spec.
**Output:** `specs/<NNN>-<slug>/plan.md`.
**Human checkpoint:** the plan is reviewed and marked `Status: approved`.

The plan enumerates every file that will be added, modified, or deleted; the tests for each AC; the warehouse-specific concerns (clustering, masking, governance, cost guardrails); and the downstream impact (semantic-layer metrics, exposures, reverse-ETL).

The warehouse preset's plan additions are appended automatically by `dbt-specify init`. Fill in the warehouse-specific tables before the plan is approved.

## Phase 3: Tasks

**Input:** an approved plan.
**Output:** `specs/<NNN>-<slug>/tasks.md`.
**Human checkpoint:** the tasks are reviewed and the engineer agrees the breakdown is right.

Tasks are ordered by dependency: sources → staging → intermediate → marts → exposures → grants → docs. Each task is small enough to be one logical commit. Each task lists its "Done when" criterion and the ACs it validates.

## Phase 4: Implement

**Input:** an approved tasks list.
**Output:** dbt project changes, one task at a time.
**Human checkpoint:** the engineer reviews and approves the final diff before merge.

`/dbt.implement` runs one task per invocation. After each task: validate, commit with the task-id message format, and stop. Never work ahead.

## The retro (not a separate phase, but mandatory)

After ship, the engineer (or agent under direction) writes a retro covering:
- What went well in the routine
- What to change for next time (CLAUDE.md updates, new skills, eval fixtures)
- Metrics: plan-phase time, implement-phase time, AI/human review findings, post-merge issues

Retros are filed as `specs/<NNN>-<slug>/retro.md` or appended to `implementation-summary.md`. CLAUDE.md and skills updates are filed as separate PRs so the methodology layer keeps improving.
