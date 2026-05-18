# SQL Server guide

Use this preset when dbt targets Microsoft SQL Server.

## What the preset adds

- clustered, nonclustered, and columnstore index planning
- incremental load and transaction log guardrails
- schema, owner, role, and access-path review
- tempdb and concurrency risk checks
- T-SQL compatibility, collation, and date precision callouts

## Good fit

- SQL Server analytics marts
- enterprise teams with strict schema and role ownership
- incremental models where blocking and log pressure matter

## Use

```bash
dbt-specify init analytics --warehouse sqlserver
```

The preset guides planning. dbt adapter configuration and database credentials remain outside
dbt-spec-kit.
