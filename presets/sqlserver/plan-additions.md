## SQL Server-specific concerns

### Index and storage design

| Model | Clustered index | Nonclustered/columnstore indexes | Justification |
|---|---|---|---|
| <model> | <cols> or heap | <cols/type> or none | <why> |

### Incremental and log impact

| Model | Strategy | Batch/log risk | Mitigation |
|---|---|---|---|
| <model> | merge / delete+insert / full refresh | low/medium/high | <plan> |

### Permissions and schemas

| Output | Schema | Owner/role | Access path |
|---|---|---|---|
| <model> | <schema> | <owner/role> | table / view / proc |

### Concurrency and tempdb

| Operation | Risk | Mitigation |
|---|---|---|
| <operation> | tempdb / blocking / spill | <plan> |
