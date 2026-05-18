## Article Q1 — Index strategy is part of model design

SQL Server tables and marts document clustered index, nonclustered indexes, or columnstore choices.
Index decisions must map to grain, joins, filters, and serving workload.

## Article Q2 — Incremental loads protect the transaction log

Large incremental models document batch size, merge/update strategy, and transaction log impact.
Full refreshes of large tables require an approved deployment window.

## Article Q3 — Schemas, ownership, and permissions are explicit

Plans name schemas, owners, grants, and downstream access paths. Restricted columns require an access
decision before implementation.

## Article Q4 — Tempdb and concurrency risks are reviewed

Large sorts, joins, snapshots, and temporary objects document tempdb/concurrency risk and mitigation.

## Article Q5 — T-SQL-specific behavior is called out

Plans name non-portable T-SQL patterns, date/time precision decisions, collations, and compatibility
level assumptions when relevant.
