# dbt project constitution

<!-- INSTRUCTIONS: This is the non-negotiable rulebook for an AI agent working on this dbt project. Every spec, plan, task, and implementation must respect these articles. Articles below the BEGIN ADDITIONS marker are warehouse-specific. -->

## Article 1 — Spec-first

No code is written before a spec is approved. The spec lives at `specs/<NNN>-<slug>/spec.md` and includes acceptance criteria in EARS format.

## Article 2 — Plan-then-implement

No code is written before a plan is approved. The plan lives at `specs/<NNN>-<slug>/plan.md` and lists every file that will be added, modified, or deleted.

## Article 3 — Human approval at each phase

A human engineer must explicitly approve the spec before planning, the plan before tasks, and the final diff before merge. AI never approves its own work.

## Article 4 — Tests are part of the work

Every model must have at least one test. Every transformation with business logic must have at least one unit test (`dbt test`-compatible unit tests, not just generic schema tests). Coverage on changed files is part of the merge bar.

## Article 5 — Grain is explicit

Every model declares its grain in a YAML doc comment. Mart-level models declare grain in the spec itself. "What is one row in this table?" must be answerable in one sentence.

## Article 6 — Source contracts are explicit

Every source is declared in `sources.yml` with `freshness`, `loaded_at_field`, and at least basic schema tests. Specs reference sources by their qualified name (`source.<name>.<table>`), not raw warehouse names.

## Article 7 — Semantic layer alignment

If a model is consumed by the semantic layer, the spec calls out which metrics and dimensions it serves. Breaking changes to semantic-layer-consumed models require a metric impact analysis in the plan.

## Article 8 — Exposures are first-class

If a model powers a dashboard, a reverse-ETL pipeline, or an API, it has a matching `exposure` entry. The plan checks downstream exposures and the implementation summary lists which exposures were affected.

## Article 9 — Naming conventions are enforced, not suggested

Staging models: `stg_<source>__<entity>.sql`. Intermediate: `int_<entity>_<purpose>.sql`. Marts: `dim_<entity>.sql` (dimension) or `fct_<process>.sql` (fact). Snapshot: `snp_<entity>.sql`. Specs that propose names violating this rule are rejected during plan review.

## Article 10 — Convention over configuration

When dbt offers multiple ways to do something, the project picks one and sticks to it. Examples: materialization choice (incremental vs. table for fact tables), test placement (in `schema.yml` vs. singular tests), macro location (`macros/` vs. inline Jinja). The convention is captured in CLAUDE.md.

## Article 11 — No silent breaking changes

A change is "breaking" if any downstream model, exposure, or semantic-layer metric would need to update. Breaking changes require: (a) explicit call-out in the spec, (b) a migration plan in the plan.md, (c) communication to affected consumers documented in the implementation summary.

## Article 12 — Retro is not optional

After every shipped feature, a retro is written to `specs/<NNN>-<slug>/retro.md` or appended to the implementation summary. The retro must answer: did the agent need clearer instructions anywhere? Did any convention need updating? Was a skill missing? Updates to CLAUDE.md or skills are filed as a separate PR.

## Article 13 — Composition with dbt-labs/dbt-agent-skills

Questions about "how does dbt work" (running tests, debugging failures, semantic layer setup, dbt Mesh) defer to `dbt-labs/dbt-agent-skills`. This constitution covers what to build and how this team builds it, not the dbt framework itself.
