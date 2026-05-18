# Athena guide

Use this preset when dbt targets Amazon Athena and S3-backed tables.

## What the preset adds

- S3 table and file-layout planning
- partitioning and partition-projection decisions
- Glue catalog and Lake Formation/IAM governance review
- workgroup, output location, and scan-cost guardrails
- Iceberg versus Hive-style table format decisions

## Good fit

- lakehouse tables queried through Athena
- Iceberg or external Hive-style datasets
- teams that need scan-cost and S3 layout evidence in PRs

## Use

```bash
dbt-specify init analytics --warehouse athena
```

dbt-spec-kit does not query Athena. dbt, the adapter, AWS credentials, and workgroup configuration
remain outside this toolkit.
