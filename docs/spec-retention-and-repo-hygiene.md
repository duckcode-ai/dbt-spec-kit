# Spec retention and repo hygiene

dbt-spec-kit is designed to preserve decision records, not every temporary note an agent creates.
Teams should keep enough context in `main` to explain why a dbt change happened, while avoiding
long-lived noise from scratch work, abandoned drafts, and local logs.

## Recommended default: balanced retention

Use balanced retention unless your team has a stronger compliance requirement.

Merge these artifacts for meaningful dbt changes:

- `specs/<NNN>-<slug>/spec.md`
- `specs/<NNN>-<slug>/plan.md`
- review evidence, such as `review.md`, `implementation-summary.md`, or a `dbt-specify report`
  summary attached to the PR

Keep `tasks.md` when the change is complex, regulated, or high-risk. For small changes, `tasks.md`
can be omitted from the final merge or archived outside the long-lived repo history after the PR is
reviewed.

## Supported retention models

| Model | What gets merged | Best for | Tradeoff |
|---|---|---|---|
| Balanced default | `spec.md`, `plan.md`, review/report summary; `tasks.md` for complex work | Most enterprise teams | Keeps decisions without storing every agent step |
| Full audit | `spec.md`, `plan.md`, `tasks.md`, `review.md`, `retro.md` for every change | Regulated or audit-heavy teams | Strongest traceability, most repo noise |
| Lean | `spec.md` plus PR/report summary for low-risk work | Small teams and low-risk fixes | Lowest noise, less implementation history |

## When to keep `tasks.md`

Keep `tasks.md` in `main` when any of these are true:

- PII, access, masking, or governance is involved
- finance, revenue, or metric definitions change
- semantic-layer objects, exposures, or contracts change
- multiple models, domains, or teams are touched
- the work needs auditability beyond the PR conversation

For low-risk implementation fixes, it is acceptable for the task breakdown to exist only during the
feature branch and PR review.

## What not to merge

Do not commit these artifacts unless a reviewer explicitly asks for them as evidence:

- raw agent scratch notes
- abandoned drafts
- temporary logs
- exploratory prompts
- local validation output files
- copied terminal output that is already summarized in PR evidence

If an agent discovers useful context during implementation, promote it into `plan.md`, `review.md`,
`findings.md`, or `CLAUDE.md` instead of keeping raw scratch notes.

## Suggested PR pattern

Normal feature PR:

```text
specs/001-customer-segmentation/spec.md
specs/001-customer-segmentation/plan.md
specs/001-customer-segmentation/review.md
models/marts/customers.sql
models/marts/customers.yml
```

High-risk PR:

```text
specs/042-revenue-definition/spec.md
specs/042-revenue-definition/plan.md
specs/042-revenue-definition/tasks.md
specs/042-revenue-definition/governance-review.md
specs/042-revenue-definition/review.md
models/marts/finance/revenue.sql
models/marts/finance/revenue.yml
```

The four-phase workflow still happens during development. The retention model decides which
artifacts remain in `main` after the work is reviewed.
