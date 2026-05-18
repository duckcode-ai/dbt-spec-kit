# /dbt.implement-all — execute approved pending tasks with checkpoints

You are implementing the remaining approved tasks in order. This command is for small, well-scoped
plans where the approved task list already names all files and validation evidence.

## Read these first
1. The current `specs/<NNN>-<slug>/tasks.md`
2. The approved `specs/<NNN>-<slug>/plan.md`
3. The approved `specs/<NNN>-<slug>/spec.md`
4. `.dbt-specify/constitution.md`
5. `CLAUDE.md`
6. Relevant `.dbt-specify/skills/` and dbt Labs skills

## Preflight

Before editing, confirm:

1. The plan is approved.
2. Every pending task has a clear "Done when" validation step.
3. The plan contains a concrete "Files to add/modify/delete" list.
4. There are no unrelated uncommitted changes in files you need to edit.
5. The work fits the approved scope.

If any preflight item fails, stop and tell the user what must be fixed.

## What to do

1. Find the first unchecked task in `tasks.md`.
2. Implement ONLY that task.
3. Run the task's validation step, `dbt parse`, and relevant `dbt test` selectors.
4. If validation passes, check the task's box `[x]`.
5. Commit using the message format `T-NN: <task description>` with a body referencing the spec,
   plan, and task paths.
6. Continue to the next unchecked task only after the prior task is committed.
7. After all tasks are complete, run:
   - `dbt-specify validate project`
   - `dbt parse`
   - `dbt-specify validate dbt --manifest target/manifest.json`, if a manifest exists
   - `dbt-specify report --format markdown`
8. Stop and summarize completed tasks, commits, validation evidence, and remaining review steps.

## Stop immediately if

- A validation command fails.
- A task requires a file not listed in the approved plan.
- A dbt model or YAML file would be edited outside the current task.
- A business rule, grain, contract, metric, or governance decision is unclear.
- You discover unrelated bugs or refactors.
- Two tasks would require conflicting edits in the same file.

## Hard rules

- Execute tasks sequentially, never in parallel.
- Do not skip tasks.
- Do not combine task commits.
- Do not add files not listed in the approved plan.
- Do not silently update the spec, plan, or task scope.
- Do not mark a task complete if validation fails.
- Do not run `/dbt.review` for yourself. Ask the user to run review after implementation.
- Never auto-merge. Human approval is the final gate.
