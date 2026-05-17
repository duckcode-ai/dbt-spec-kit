# /dbt.specify — draft a spec from a feature description

You are helping a dbt practitioner write a spec for a new feature or change.

## Read these first
1. `.dbt-specify/constitution.md` — the project's non-negotiable principles
2. `CLAUDE.md` — this project's conventions
3. `.dbt-specify/templates/spec-template.md` — the spec format

## What to do

Given the user's feature description:

1. Determine if this is a staging model, a mart, or something else. Load the relevant skill:
   - Staging: `.dbt-specify/skills/writing-staging-model-specs/SKILL.md`
   - Mart: `.dbt-specify/skills/writing-mart-specs-with-grain/SKILL.md`
   - Cross-system entity work: `.dbt-specify/skills/writing-business-glossary-specs/SKILL.md`

2. Generate the next spec number by listing `specs/` and incrementing the highest existing `<NNN>-` prefix.

3. Create `specs/<NNN>-<slug>/spec.md` from the template, filling in every section. Use information from the user's description; for anything not provided, ask one clarifying question per missing critical field. Maximum three clarifying questions total.

4. Write ACs in EARS format. Run `dbt-specify validate specs/<NNN>-<slug>/spec.md` to verify.

5. Tell the user the spec is ready for review and which file to open.

## Hard rules

- Do NOT write any code, models, tests, or YAML during this phase.
- Do NOT propose a plan during this phase.
- If the description is vague (e.g., "improve performance"), refuse and ask for specifics.
