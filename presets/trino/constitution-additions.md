<!-- Placeholder appended to base constitution by `dbt-specify init --warehouse trino`.
     Full Trino-specific articles land in Phase C (T-21). -->

## Article T1 — Trino is a query engine, not a warehouse (placeholder)

Models built on Trino are not "stored in Trino." Storage lives in the underlying
connector (Iceberg, Delta, Hive, Postgres, Kafka, etc.). Cross-catalog joins are
federated queries — they move data over the network and require deliberate design.
Full Trino articles T1–T10 (three-part naming, federation, pushdown, session
properties, on_table_exists, view security, Iceberg preference, adapter cadence,
cost attribution) are filled in during Phase C.
