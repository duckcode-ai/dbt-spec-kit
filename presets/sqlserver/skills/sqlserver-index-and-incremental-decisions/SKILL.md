---
name: sqlserver-index-and-incremental-decisions
description: Use when planning SQL Server dbt index, columnstore, incremental, and concurrency decisions.
---

# SQL Server index and incremental decisions

## When to use this skill

Use this for SQL Server marts, incremental models, large joins, or governed outputs.

## Decision routine

1. Confirm the table grain and primary serving query.
2. Choose clustered rowstore, clustered columnstore, or heap deliberately.
3. Add nonclustered indexes only for named joins, filters, or uniqueness checks.
4. For incremental models, document merge key, batch size, and transaction log risk.
5. Check whether large operations can stress tempdb or block concurrent readers.
6. Document schemas, ownership, grants, and restricted column access.

## Common failures

- Clustered index does not match the grain or access pattern.
- Large `MERGE` operations with no batch/log plan.
- Columnstore used on small or highly volatile tables by reflex.
- Hidden collation/date precision changes in mart outputs.
