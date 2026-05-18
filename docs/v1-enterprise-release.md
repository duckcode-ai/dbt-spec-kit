# v1 enterprise release

v1 turns dbt-spec-kit from a methodology starter kit into an enterprise trust layer for AI-assisted
dbt delivery.

## Product promise

Agents can help specify, plan, task, and implement dbt changes, but humans approve the intent and CI
proves the agent followed the contract.

## Release pillars

| Pillar | v1 capability |
|---|---|
| Controlled autonomy | `/dbt.specify`, `/dbt.plan`, `/dbt.tasks`, `/dbt.implement`, `/dbt.analyze`, `/dbt.review` |
| Enforcement | `validate project`, `validate dbt`, `doctor`, `report`, `ci` |
| Enterprise adoption | Brownfield guide, CI guide, PR evidence reports |
| Warehouse depth | Snowflake, Databricks, Trino, BigQuery presets |

## Definition of done

- A data platform lead can initialize the kit in an existing dbt repo.
- A team can require dbt-spec-kit validation in CI.
- A PR can show traceability from ACs to plan, tasks, and dbt artifact evidence.
- Warehouse-specific guardrails are included in the generated constitution and plan template.
- The project remains agent-neutral and does not require a hosted service.
