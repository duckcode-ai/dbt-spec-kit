---
name: athena-partition-file-layout-decisions
description: Use when planning Athena dbt models that depend on S3 layout, partitions, Glue/Lake Formation governance, and scan cost.
---

# Athena partition and file-layout decisions

## When to use this skill

Use this for Athena-backed dbt models, especially large tables, Iceberg tables, external sources, or
governed S3 data.

## Decision routine

1. Choose table format deliberately: Iceberg for managed evolution/upserts, Hive-style external
   tables for simple append/read patterns.
2. Prefer columnar files such as Parquet or ORC.
3. Document partition columns and expected pruning predicates.
4. Check small-file risk and compaction expectations.
5. Name Glue database/table ownership and Lake Formation or IAM access boundaries.
6. Name workgroup, query result location, and scan cost guardrails.

## Common failures

- Partitioning by a high-cardinality column that creates too many S3 prefixes.
- Generating many tiny files that make every query expensive.
- Running unbounded scans because partition projection was not planned.
- Publishing governed outputs without Glue/Lake Formation ownership review.
