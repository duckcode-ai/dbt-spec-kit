---
name: writing-staging-model-specs
description: Use when writing the spec for a new dbt staging model (`stg_<source>__<entity>.sql`).
---

# Writing specs for dbt staging models

## When to use this skill

You're spec'ing a model in `models/staging/`. Staging models have a narrow, well-defined job — this skill keeps the spec tight.

## What a staging model does (and doesn't)

Staging models do:
- Rename columns to project conventions (snake_case, conventional suffixes like `_at`, `_id`)
- Cast types
- Filter out obvious junk (test rows, deletes, soft deletes)
- Generate surrogate keys via `dbt_utils.generate_surrogate_key`
- Apply masking for PII at the staging layer (never at the mart)

Staging models do NOT:
- Join across sources
- Compute business metrics
- Aggregate (one row in = one row out)
- Apply business logic that may change

## Template (additions to the base spec template)

```markdown
## Source

| Field | Value |
|---|---|
| Loader | <fivetran|airbyte|kafka|custom> |
| Source schema | `<raw_schema>` |
| Source table | `<table>` |
| Refresh cadence | <hourly|daily|...> |
| Loaded-at field | `<column>` |

## Column mapping

| Source column | Renamed to | Type cast | Notes |
|---|---|---|---|
| `id` | `<entity>_id` | `bigint` | natural key |
| `created_at` | `<entity>_created_at` | `timestamp_tz` | |
| `email` | `email_masked` | `string` | masked via policy `<name>` |

## Filter rules

- Drop rows where `<col> = '<test_marker>'`
- Drop rows where `is_deleted = true` (soft delete handling)
```

## Acceptance criteria patterns

Staging-flavored ACs that should always be present:

- AC: The system shall enforce uniqueness on `<entity>_id`.
- AC: The system shall enforce not-null on `<entity>_id` and `<entity>_created_at`.
- AC: When the source table receives a soft-deleted row, the system shall exclude it from the staging output.
- AC: Where PII columns exist, the system shall apply the masking policy `<name>`.

## Anti-patterns

- **Joining in staging** — push the join to intermediate or mart.
- **Computing metrics in staging** — push to mart.
- **Renaming in mart instead of staging** — rename once, at the staging boundary.
- **Skipping the loaded-at field declaration** — freshness tests break silently.
