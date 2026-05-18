---
name: azure-sql-service-tier-decisions
description: Use when planning Azure SQL dbt work that affects service tier, elastic pools, indexing, security, or workload pressure.
---

# Azure SQL service tier and workload decisions

## When to use this skill

Use this when dbt runs against Azure SQL Database, Azure SQL Managed Instance, or an Azure SQL-backed
analytics serving database.

## Decision routine

1. Identify service tier, elastic pool, and expected workload pressure.
2. Use Query Store or representative query plans to justify performance-sensitive changes.
3. Choose indexes and columnstore based on query patterns and data volume.
4. Plan incremental loads around transaction log and concurrency limits.
5. Use Azure-native access controls for governed data: roles, views, RLS, or dynamic data masking.
6. Document network/private endpoint and deployment-window constraints.

## Common failures

- Treating Azure SQL like a limitless warehouse.
- Full refreshing large marts in a shared elastic pool without a window.
- Adding indexes that help dbt but hurt application writes.
- Missing RLS or masking decisions for governed outputs.
