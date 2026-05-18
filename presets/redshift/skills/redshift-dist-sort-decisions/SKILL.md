---
name: redshift-dist-sort-decisions
description: Use when choosing Redshift distribution, sort, maintenance, and Spectrum patterns for dbt models.
---

# Redshift distribution and sort decisions

## When to use this skill

Use this for Redshift tables, incremental models, large marts, or models joining internal and
external data.

## Decision routine

1. Identify the largest table and the most common join key.
2. Choose distribution style deliberately: `AUTO` for uncertain/simple cases, `KEY` for stable large
   joins, `ALL` only for small dimensions, `EVEN` when no join key dominates.
3. Choose sort keys for the dominant filter range, usually a date/timestamp or a stable business key.
4. For incremental models, document whether `VACUUM` and `ANALYZE` are needed.
5. For Spectrum sources, verify partition pruning and avoid large unbounded external joins.
6. Document grants, schemas, and late binding view decisions for governed outputs.

## Common failures

- Distribution key chosen from a column that is not used in the large join.
- Sort key chosen from load order instead of query predicates.
- External table scans without a partition boundary.
- Append-heavy incremental tables with no maintenance plan.

## Output

Return distribution, sort, maintenance, and external-access recommendations with review evidence.
