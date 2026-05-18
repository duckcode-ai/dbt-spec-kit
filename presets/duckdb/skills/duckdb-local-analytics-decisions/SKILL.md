---
name: duckdb-local-analytics-decisions
description: Use when planning DuckDB dbt work around local files, Parquet, extensions, memory, and CI reproducibility.
---

# DuckDB local analytics decisions

## When to use this skill

Use this for local analytics, CI fixtures, Parquet-first workflows, and lightweight dbt projects that
target DuckDB.

## Decision routine

1. List every local file, object-store path, or generated artifact.
2. Confirm whether each path exists in CI or is local-only.
3. Estimate data size and memory pressure.
4. Use Parquet staging for large repeated reads.
5. Document required DuckDB extensions and install behavior.
6. Treat file outputs with PII as governed artifacts.

## Common failures

- Plans that work only on one developer's absolute file path.
- Loading large CSVs repeatedly instead of staging Parquet.
- Using extensions without CI setup.
- Exporting PII to local files without a handling decision.
