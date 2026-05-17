# /dbt.plan — propose a plan from an approved spec

You are turning an approved spec into a file-by-file plan.

## Read these first
1. The current spec at `specs/<NNN>-<slug>/spec.md` (find the latest)
2. `.dbt-specify/constitution.md`
3. `.dbt-specify/templates/plan-template.md`
4. Existing repo structure: `models/`, `tests/`, `seeds/`, `macros/`, `_governance/`, `analyses/`

## What to do

1. Confirm the spec is marked **approved**. If not, refuse and tell the user to approve it first.

2. Generate `specs/<NNN>-<slug>/plan.md` from the template. For each section:
   - **Architecture** — 2–4 sentences referencing constitution articles
   - **Files to add/modify/delete** — exhaustive; one row per file
   - **Tests** — every AC must map to at least one test
   - **Risks** — at least two; one mitigated, one open
   - **Downstream impact** — search for exposures, semantic-layer references, reverse-ETL configs

3. The plan must respect the warehouse preset additions appended at the bottom of `plan-template.md`. Fill those tables in.

4. Open questions go in "Open questions for review" — do NOT silently make assumptions.

5. Mark the plan as **proposed** and tell the user to review and either approve or send back for revision.

## Hard rules

- Do NOT write any models or YAML during this phase.
- Do NOT skip the "Files to delete" section even if empty — write "(none)" if so.
- Every file in "Files to add" must trace to at least one AC.
