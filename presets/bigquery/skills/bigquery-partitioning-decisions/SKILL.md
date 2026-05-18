# BigQuery partitioning decisions

Use this skill when writing or reviewing specs and plans for BigQuery models that may be large,
dashboard-facing, or cost-sensitive.

## Decision routine

1. Identify the dominant query predicate: event date, load date, account/customer, region, or another
   business key.
2. Prefer partitioning by date or timestamp when routine queries scan bounded time windows.
3. Add clustering for high-cardinality columns used in joins or filters after the partition boundary.
4. Document unpartitioned tables explicitly; "small enough" is acceptable only with a size estimate.
5. For incremental models, specify the unique key, incremental predicate, and late-arriving data
   behavior.
6. For PII columns, call out policy tags or authorized views in the plan.

## Spec prompts

- What is one row in this table?
- What time field controls routine scans?
- What is the largest expected scan in a normal production run?
- Which dashboard, metric, ML feature, or reverse-ETL job consumes the model?
- Which columns require policy tags or authorized views?
