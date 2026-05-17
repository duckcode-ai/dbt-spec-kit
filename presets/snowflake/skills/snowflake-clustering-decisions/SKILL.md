---
name: snowflake-clustering-decisions
description: Use when deciding whether and how to add a clustering key to a Snowflake-backed dbt model.
---

# Choosing clustering keys for Snowflake dbt models

## When to use this skill

You're proposing a new model or modifying an existing one, and need to decide whether to add `config(cluster_by=[...])`. Use this skill to make the decision deliberately rather than by reflex.

## The decision rules

**Add a clustering key if all of these are true:**
1. The table will exceed 1 GB compressed (estimate from source row count × avg row size).
2. The most common query predicates include a column with high cardinality and natural temporal/categorical ordering (often `event_date`, `customer_id`, `region`).
3. The table is queried more often than rebuilt. (Clustering costs reorganization on insert.)

**Skip clustering if any of these are true:**
1. Table is < 1 GB compressed.
2. Table is rebuilt full every run (clustering is wasted).
3. Predicates are unpredictable (e.g., ad-hoc analytics tables).

## How to pick the key

- One column is usually better than three. Snowflake docs say up to 4, but maintenance cost rises sharply.
- Prefer the column most often used in `WHERE` and `JOIN`.
- For event/fact tables, `event_date` (or a derived `event_month` for very large tables) is the conventional choice.
- For wide dimension tables, the natural primary join key is usually right.

## How to verify the choice

After the model is built, run a representative query and check the `Partitions scanned` vs. `Partitions total` in the query profile. A well-clustered table scans <10% of partitions for selective predicates.

```sql
-- example: check clustering health on a real query
SELECT system$clustering_information('analytics.fct_orders', 'order_date');
```

## Anti-patterns

- **Clustering on `created_at` when queries filter on `event_date`** — keys must match query patterns, not row insertion patterns.
- **Clustering tables under 1 GB** — adds maintenance overhead with no scan benefit.
- **Clustering on a surrogate key** — high cardinality but rarely used in `WHERE`; usually wrong.
- **Three-column clustering on a small dimension** — premature optimization.

## In the spec/plan

The plan's "Clustering decisions" table should justify the choice for each table >1 GB. Reviewers check the justification, not just that a key is present.
