# Redshift guide

Use this preset when dbt runs on Amazon Redshift or Redshift is the analytics serving database.

## What the preset adds

- distribution and sort key planning
- vacuum and analyze expectations
- Spectrum/external table scan boundaries
- workload queue and full-refresh cost guardrails
- schema, grants, late binding view, and restricted-data review

## Good fit

- enterprise marts on Redshift
- Redshift Spectrum plus internal table joins
- teams that need PR evidence for dist/sort decisions

## Use

```bash
dbt-specify init analytics --warehouse redshift
```

dbt still owns execution through the Redshift adapter and the user's normal profile. This preset only
changes planning guidance and generated agent context.
