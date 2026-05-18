# dbt-specify CI report

## Summary

- Errors: 0
- Warnings: 0
- Info: 1

## Findings

- **INFO [EXAMPLE_REPORT]**: Example report for a completed enterprise customer 360 PR. A real run is generated with `dbt-specify report --format markdown`.

## Evidence

| Check | Result |
|---|---|
| `dbt-specify validate project` | pass |
| `dbt parse` | pass |
| `dbt-specify validate dbt --manifest target/manifest.json` | pass |
| `dbt build --select +dim_customers+` | pass |
| Duplicate-resolution unit test | pass |
