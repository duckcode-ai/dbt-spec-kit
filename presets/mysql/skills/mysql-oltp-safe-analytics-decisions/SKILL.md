---
name: mysql-oltp-safe-analytics-decisions
description: Use when planning MySQL dbt work that must protect OLTP systems, indexes, locks, and incremental loads.
---

# MySQL OLTP-safe analytics decisions

## When to use this skill

Use this when MySQL is a source or target for dbt and the workload might affect operational systems.

## Decision routine

1. Confirm whether dbt reads a primary, replica, or analytics copy.
2. Require indexes for large joins, filters, and uniqueness checks.
3. Use `EXPLAIN` expectations for heavy queries.
4. Prefer incremental loads with watermarks over repeated full refreshes.
5. Document lock risk, batch size, and deployment window.
6. Call out engine, charset, collation, and timezone assumptions that affect output semantics.

## Common failures

- Running analytic joins on a production primary.
- Full refreshing a large table during business hours.
- Comparing text across unexpected collations.
- Forgetting timezone conversion for order/event dates.
