---
name: reviewing-ci-evidence
description: Use when deciding whether a dbt PR has enough validation evidence to merge after AI-assisted implementation.
---

# Reviewing CI evidence

## When to use this skill

Use this before final review and before marking a task or PR complete.

## Minimum evidence

- `dbt-specify validate project`
- `dbt parse`
- `dbt-specify validate dbt --manifest target/manifest.json` when a manifest exists
- `dbt-specify report --format markdown`
- dbt tests selected for changed models and downstream consumers
- Human sign-off for any untestable AC

## Review routine

1. Check that every validation command named in `tasks.md` has a result.
2. Check that failures are fixed, not ignored.
3. Confirm skipped commands have a stated reason and human acceptance.
4. Compare the final report against the AC list.
5. Block merge if lifecycle checks or required dbt tests failed.

## Output

Return a merge evidence summary:

| Evidence | Result | Notes |
|---|---|---|

End with one recommendation: approve, request changes, or block.
