## Azure SQL-specific concerns

### Service tier and workload

| Database/pool | Tier | Workload risk | Guardrail |
|---|---|---|---|
| <db/pool> | <tier> | CPU / IO / log / none | <plan> |

### Index and incremental strategy

| Model | Index/columnstore plan | Incremental strategy | Log risk |
|---|---|---|---|
| <model> | <indexes> | merge / delete+insert / full refresh | low/medium/high |

### Security and access

| Output | Role/access path | RLS/DDM/view boundary | Reviewer |
|---|---|---|---|
| <model> | <role> | <boundary> | <owner> |

### Operational constraints

| Constraint | Impact | Mitigation |
|---|---|---|
| firewall/private endpoint/cross-db/tempdb | <impact> | <plan> |
