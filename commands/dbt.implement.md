# /dbt.implement — execute the next pending task

You are implementing one task from an approved tasks list.

## Read these first
1. The current `tasks.md`
2. The plan and spec it's derived from
3. `.dbt-specify/constitution.md`
4. The warehouse preset constitution additions (relevant to your warehouse)

## What to do

1. Find the next unchecked task in `specs/<NNN>-<slug>/tasks.md`.

2. Implement ONLY that task. Do not work ahead.

3. After implementation:
   - Run the validation step in the task's "Done when"
   - Run `dbt parse` to confirm the project still compiles
   - Run any relevant `dbt test` selectors
   - Check the task's box `[x]`
   - Stage and commit using the message format: `T-NN: <task description>` (commit body references the spec/plan paths)

4. Tell the user the task is complete and what's next.

## Hard rules

- Implement exactly one task per invocation.
- Do NOT add files not listed in the plan. If you discover a missing file, surface it to the user — do not create it silently.
- Do NOT modify files outside the plan's "Files to add/modify/delete" list. If you find a real bug elsewhere, write it to `specs/<NNN>-<slug>/findings.md` and continue.
- Do NOT mark the task complete if validation fails.
- Never auto-merge. Human approval is the final gate.
