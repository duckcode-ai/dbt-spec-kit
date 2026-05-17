---
name: databricks-liquid-clustering-decisions
description: Use when deciding the clustering column(s) for a Databricks-backed dbt model using Liquid Clustering.
---

# Choosing Liquid Clustering for Databricks dbt models

## When to use this skill

You're configuring a new table on Databricks via dbt and need to decide between: no clustering, Liquid Clustering, or (rarely now) classic partitioning.

## The decision rules

**Use Liquid Clustering if:**
1. Table will be queried with selective predicates on one or more columns.
2. You don't have perfect foresight on the access pattern (Liquid is more forgiving than partitioning).
3. Table will grow over time and write patterns may shift.

**Skip clustering if:**
1. Table is small (<1 GB) and queries are unselective.
2. Table is rebuilt full every run.

**Use classic partitioning only if:**
1. You have a strong, stable query predicate that aligns to a natural temporal column.
2. You're on a runtime that doesn't support Liquid Clustering yet.

## How to pick clustering columns

- Up to 4 columns supported; one is usually enough.
- Prefer columns frequently in `WHERE` and `JOIN` keys.
- High-cardinality columns benefit more than low-cardinality ones.
- For fact tables, `event_date` is a frequent winner. For wide dimensions, the natural surrogate key.

## How to verify

After build, check the table properties:

```sql
DESCRIBE TABLE EXTENDED <catalog>.<schema>.<table>;
-- look for clusteringColumns property
```

Run a representative selective query and check the Spark UI for files pruned.

## Anti-patterns

- **Clustering on every selectable column** — diminishing returns past 1–2 columns.
- **Liquid Clustering on a small reference table** — useless overhead.
- **Mixing classic partitioning and Liquid Clustering** — pick one per table.
- **Clustering on a column that's masked** — masking happens before clustering, so the clustering benefit disappears.

## Predictive Optimization

Liquid Clustering composes with Predictive Optimization. Verify PO is enabled at the schema level:

```sql
ALTER SCHEMA <catalog>.<schema> ENABLE PREDICTIVE OPTIMIZATION;
```

## In the spec/plan

The plan's "Liquid Clustering decisions" table justifies each clustering column. Reviewers check the justification matches the query pattern in the spec's "Constraints" section.
