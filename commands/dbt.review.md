# /dbt.review — review the final diff against the approved plan

You are reviewing a dbt change after implementation and before human merge approval.

## Read these first
1. The current `specs/<NNN>-<slug>/spec.md`
2. The current `specs/<NNN>-<slug>/plan.md`
3. The current `specs/<NNN>-<slug>/tasks.md`
4. `git diff --name-only`
5. `target/manifest.json`, if present

## What to do

1. Run `dbt-specify validate project`.
2. Run `dbt-specify validate dbt` if a manifest exists.
3. Compare changed files to the plan's Files to add/modify/delete sections.
4. Confirm all tasks are checked or list the unfinished tasks.
5. Summarize dbt validation evidence: `dbt parse`, relevant `dbt build`, relevant `dbt test`.
6. Produce a concise review with findings first, then residual risks.

## Hard rules

- Do NOT auto-merge.
- Do NOT approve changes outside the plan unless the plan was updated and approved.
- Do NOT mark validation as complete if dbt commands or dbt-specify checks failed.
