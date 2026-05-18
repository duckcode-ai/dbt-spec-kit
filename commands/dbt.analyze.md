# /dbt.analyze — validate spec, plan, and task traceability

You are checking whether the current dbt-spec-kit workflow is ready for implementation.

## Read these first
1. The current `specs/<NNN>-<slug>/spec.md`
2. The current `specs/<NNN>-<slug>/plan.md`, if present
3. The current `specs/<NNN>-<slug>/tasks.md`, if present
4. `.dbt-specify/constitution.md`

## What to do

1. Run `dbt-specify validate project`.
2. Report all release-blocking errors first.
3. Check that every AC in the spec is referenced by the plan and tasks.
4. Check that implementation has not started before spec and plan approval.
5. If `target/manifest.json` exists, run `dbt-specify validate dbt`.
6. Tell the user whether implementation can proceed.

## Hard rules

- Do NOT write dbt code in this command.
- Do NOT silently approve missing traceability.
- If validation fails, stop and explain the exact artifact to fix.
