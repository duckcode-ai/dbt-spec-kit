# MotherDuck guide

Use this preset when dbt targets MotherDuck or a hybrid DuckDB/MotherDuck workflow.

## What the preset adds

- local versus cloud execution boundary review
- database, share, role, and collaborator planning
- file and object-store reproducibility checks
- cost/quota guardrails
- sensitive data movement review

## Good fit

- collaborative DuckDB-style analytics
- shared demo and lightweight team projects
- local-to-cloud workflows where data movement must be explicit

## Use

```bash
dbt-specify init analytics --warehouse motherduck
```

The preset does not configure MotherDuck authentication. It only adds planning and governance
guidance.
