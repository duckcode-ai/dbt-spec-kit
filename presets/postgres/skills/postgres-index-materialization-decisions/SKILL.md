---
name: postgres-index-materialization-decisions
description: Use when planning Postgres dbt materializations, indexes, lock risk, and OLTP-safe execution.
---

# Postgres index and materialization decisions

## When to use this skill

Use this for Postgres-backed dbt models, especially when the database may also support application
traffic.

## Decision routine

1. Confirm whether dbt runs against a primary, replica, or dedicated analytics database.
2. Prefer tables or incremental models for expensive joins used by dashboards.
3. Add indexes only when they support a named join, filter, uniqueness check, or serving query.
4. For materialized views, document refresh strategy and lock impact.
5. For large rebuilds, document transaction/lock risk and acceptable deployment window.
6. Keep grants and schemas explicit for governed marts.

## Common failures

- Running heavy transformations on an operational primary without a guardrail.
- Creating views over expensive joins that every dashboard reruns.
- Adding broad indexes without a query pattern.
- Refreshing a materialized view during peak application traffic.
