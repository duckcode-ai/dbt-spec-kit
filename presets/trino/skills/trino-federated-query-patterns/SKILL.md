---
name: trino-federated-query-patterns
description: Use when designing a dbt-trino model that touches more than one Trino catalog, or when deciding whether a model should push work down to the underlying connector vs. pull into Trino.
---

# Federated query patterns on Trino

## When to use this skill

You're designing a model that touches more than one Trino catalog, OR you're trying to decide whether to make Trino compute something or push it back to the source. Both decisions are easy to get wrong by reflex and expensive to fix later.

## Mental model: Trino moves data, the connector stores it

Trino is a query engine. Storage lives in the underlying connectors:

- `iceberg` catalog → Parquet files in object storage, Iceberg table format
- `hive` catalog → files in object storage, Hive metastore
- `postgresql` catalog → an actual Postgres database
- `kafka` catalog → topic data via Kafka brokers
- `mongodb`, `elasticsearch`, etc. → analogous

The "warehouse" framing from Snowflake/Databricks doesn't apply. Every Trino model is a query plan that traverses these connectors and assembles results in Trino's memory. The question is always: *where is the work actually happening?*

## Decision 1: should this be a cross-catalog query at all?

**Prefer keeping the join inside one catalog when possible.** Cross-catalog joins:
- Move data over the network into Trino's coordinator/worker memory
- Defeat connector-side optimizations (Postgres index scans, Iceberg partition pruning of the other side)
- Make cost attribution harder

**Cross-catalog queries are fine when:**
1. The data really does live in different systems and no upstream pipeline can land it together
2. The non-Iceberg side is small (a dimension table, a config lookup)
3. You're in a lakehouse model that intentionally federates

**Cross-catalog queries are usually wrong when:**
1. The non-Iceberg side is large and you could `INSERT INTO iceberg.*.* SELECT FROM` it first
2. You're doing this "because Trino can" rather than because it's the best design
3. The same join pattern appears in 5+ marts (build a staged Iceberg table instead)

## Decision 2: pushdown — what work is the connector actually doing?

The cost difference between Trino-side filtering and connector-side filtering can be 1000x for large tables. The answer is in `EXPLAIN`.

### How to check pushdown

```sql
EXPLAIN (TYPE DISTRIBUTED)
SELECT count(*) FROM postgresql.public.orders WHERE created_at > date '2026-01-01';
```

In the output, look for:
- **`ScanFilterProject`** → filter is being applied by the connector (good)
- **`ScanProject` followed by `Filter` in a later stage** → connector returned all rows; Trino filtered after (bad)

### What typically pushes down

- Simple predicates on indexed columns (Postgres, MySQL): yes
- Predicates on partition columns (Iceberg, Hive): yes
- Aggregations on Iceberg with statistics: yes (Trino can sometimes answer `count(*)` from metadata)
- Joins to a small Trino-side table: usually does NOT push down (dynamic filtering helps)

### What typically does NOT push down

- Predicates on computed columns (`WHERE upper(name) = 'X'` against Postgres)
- Predicates involving Trino-specific functions
- Complex expressions involving multiple columns

## Decision 3: how to materialize for federation patterns

If a downstream model joins across catalogs frequently, **materialize the smaller side into Iceberg first.** This trades one batch write for many cheap reads.

```python
{{ config(
    materialized='table',
    catalog='iceberg',
    schema='cross_system',
    on_table_exists='rename'
) }}
SELECT customer_id, region, plan_tier
FROM postgresql.public.customer_profile
WHERE is_active = true
```

Then downstream marts join `iceberg.cross_system.customer_profile_cached` instead of the live Postgres source.

## Anti-patterns

- **Six-way join across six catalogs** — your plan is wrong; rebuild as a staged pipeline.
- **`WHERE source_data_lake.events.event_date > current_date - 7` without verifying pushdown** — silently scans the full table.
- **Materializing a Postgres-source model as a view** — every dashboard hit becomes a live Postgres query; usually wrong.
- **Joining a Kafka catalog to anything large** — Kafka connector reads sequentially; do not join to large catalogs.
- **Using `kafka.*.*` as a source without checking the connector's offset behavior** — re-reading topics in dbt is a foot-gun.

## In the spec/plan

The plan's "Cross-catalog joins" table makes every federation point visible. The "Pushdown plan" table makes every potentially-expensive predicate explicit. Reviewers verify `EXPLAIN` output is in the plan or attached.
