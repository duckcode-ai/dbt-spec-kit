# Implementation summary — Jaffle Shop staging overhaul

**Date shipped:** 2026-05-17
**Lead time (spec to prod):** 4 hours

## Outcome

All seven ACs verified. Three legacy staging models replaced. Three marts updated. Old files deleted. CI green. No row-count regressions.

## What went well

- **Plan-first paid off.** The "Files to delete" table forced the agent to confront the downstream mart updates BEFORE writing code. In a vibe-coded version we would have deleted the old staging models first, broken the marts, then scrambled.
- **AC7 (row count preservation) caught a real bug.** The agent initially generated a surrogate key using `dbt_utils.generate_surrogate_key(['email'])` — but `email` is NULL for some test rows, so the surrogate key was non-deterministic. The row count test caught it; the fix was to include `customer_id` in the surrogate key inputs.

## What to change for next time

- **CLAUDE.md update:** Add an explicit rule that surrogate key inputs must include the natural primary key, never just business attributes. Filed as PR #<placeholder>.
- **New skill:** A `surrogate-key-generation` skill that captures this rule and the failure mode. Filed as PR #<placeholder>.

## Metrics

| Metric | Value |
|---|---|
| Plan-phase time | 25 minutes (mostly waiting for human review) |
| Implement-phase time | 1 hour 15 minutes |
| AI review findings | 2 (both fixed pre-merge) |
| Human review findings | 1 (the surrogate key issue caught by AC7) |
| Post-merge issues | 0 |

## Updates filed

- [x] CLAUDE.md change: PR #<placeholder>
- [x] New skill: PR #<placeholder>
- [x] Eval fixture for the surrogate-key edge case: PR #<placeholder>
