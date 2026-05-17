---
name: writing-mart-specs-with-grain
description: Use when writing the spec for a dbt mart-layer model (`dim_*`, `fct_*`, or aggregated mart).
---

# Writing specs for dbt mart models — grain is everything

## When to use this skill

You're spec'ing a mart-layer model. The single most common failure mode for mart models is grain ambiguity — "what is one row in this table?" doesn't have a clean answer.

## The grain question must be answered first

Before anything else, the spec answers this in one sentence:

> One row in this table represents <one specific business event or entity>.

Examples:
- "One row represents one completed order at the time the order shipped."
- "One row represents one customer's state on a given day (daily snapshot)."
- "One row represents one session, where a session is defined as activity from one user with gaps no longer than 30 minutes."

If you can't answer in one sentence, the model needs to be split into two.

## Template (additions to the base spec template)

```markdown
## Grain

**One row represents:** <one specific business event or entity>

**Grain columns (unique key):** <col1, col2, col3>

**Type:** <event fact | snapshot fact | dimension (Type 1 / Type 2)>

## SCD strategy (dimensions only)

| Field | Type 1 (overwrite) | Type 2 (history) |
|---|---|---|
| `customer_name` | x | |
| `customer_tier` | | x |

## Late-arriving data handling

<How does the model handle records that arrive after the partition has already been processed? Reprocess window? Reject? Re-key?>

## Semantic layer alignment

| Metric / dimension | Provided by this model? | Notes |
|---|---|---|
| `total_revenue` | yes | sum of `order_amount` |
| `customer_tier` | yes (as a dim) | |
```

## Acceptance criteria patterns

- AC: The system shall enforce uniqueness on `<grain_cols>`.
- AC: When a source row arrives <N> days late, the system shall <reject | reprocess | append-only>.
- AC: Where this model feeds the semantic layer metric `<name>`, the system shall preserve the column `<col>` with stable name and type.

## Anti-patterns

- **Mart that combines multiple grains** — split into separate marts.
- **Grain that changes silently** — adding a new join key without spec change is a Constitution §11 violation.
- **No explicit late-arriving-data policy** — silent inconsistency follows.
- **Mart with `is_current` flag and no SCD strategy declared** — pick Type 2 with `valid_from`/`valid_to` instead.
