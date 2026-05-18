# Postgres guide

Use this preset when dbt targets Postgres or uses Postgres as an analytics-safe serving database.

## What the preset adds

- OLTP safety checks for primary versus replica versus analytics database
- index and materialization planning
- lock and transaction impact review
- schema/grant/access planning
- extension and non-portable SQL callouts

## Good fit

- smaller analytics projects on Postgres
- product analytics replicas
- local or self-managed dbt deployments where lock safety matters

## Use

```bash
dbt-specify init analytics --warehouse postgres
```

The preset does not connect to Postgres. dbt and its adapter handle database execution.
