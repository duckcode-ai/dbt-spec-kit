# Brownfield onboarding

Most enterprise dbt projects are already in production. dbt-spec-kit is designed to be adopted
incrementally without rewriting existing models.

## 1. Inspect the repo

```bash
cd path/to/dbt-project
dbt-specify doctor
```

The doctor command reports missing adoption pieces such as `.dbt-specify/`, `CLAUDE.md`, `specs/`,
`target/manifest.json`, and model documentation/test inventory.

If your team wants a low-risk practice run first, use the
[jaffle-shop AI SDLC walkthrough](jaffle-shop-ai-sdlc-walkthrough.md). It shows the same adoption
steps on the upstream dbt Labs example project before you apply the process to production code.

## 2. Initialize the methodology layer

```bash
dbt-specify init analytics --warehouse snowflake
```

If `CLAUDE.md` already exists, dbt-spec-kit writes `CLAUDE.md.dbt-specify-suggested` so you can merge
the guidance manually.

## 3. Start with new work only

Do not rewrite the whole dbt repo to satisfy the new constitution on day one. Apply the workflow to
the next meaningful feature:

1. `/dbt.specify <feature>`
2. approve `spec.md`
3. `/dbt.plan`
4. approve `plan.md`
5. `/dbt.tasks`
6. `/dbt.implement`
7. `/dbt.review`

## 4. Add CI in warning-first mode

Run:

```bash
dbt-specify report --format markdown
```

Use the report as PR evidence first. Once false positives are fixed and team conventions are clear,
switch to `dbt-specify ci` as a required check.

For a rollout meeting format, see the [team onboarding playbook](team-onboarding-playbook.md).
