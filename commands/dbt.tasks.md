# /dbt.tasks — decompose an approved plan into ordered tasks

You are turning an approved plan into a sequenced work breakdown.

## Read these first
1. The current plan at `specs/<NNN>-<slug>/plan.md`
2. `.dbt-specify/templates/tasks-template.md`

## What to do

1. Confirm the plan is marked **approved**. If not, refuse.

2. Generate `specs/<NNN>-<slug>/tasks.md` from the template.

3. Tasks are ordered by dependency:
   - sources.yml additions → staging models → intermediate → marts → exposures → grants → docs
   - Within each layer, alphabetical or by data flow

4. Each task has:
   - A unique id (T-01, T-02, ...)
   - An imperative one-line description
   - A "Done when" criterion that's observable
   - A "Validates" AC reference

5. Each task is small enough to commit as one logical change.

6. Tell the user the tasks are ready and they should approve before implementation.

## Hard rules

- Do NOT skip ahead to implementation in this phase.
- If a task feels larger than "one commit", split it.
- If a task can run in parallel with another, mark it `[P]` at the end of the description.
