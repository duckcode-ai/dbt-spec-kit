<!-- INSTRUCTIONS:
  This plan is approved BEFORE any code is written.
  List every file that will be added, modified, or deleted.
  Call out warehouse-specific concerns in the warehouse sections (Snowflake/Databricks).
-->

# Plan — <feature title>

**Spec:** ../spec.md
**Author:** <agent name + reviewer>
**Date:** <YYYY-MM-DD>
**Status:** proposed | approved | superseded

## Architecture

<2–4 sentences. The shape of the solution. Reference any relevant constitution articles.>

## Files to add

| Path | Purpose |
|---|---|
| `models/staging/<source>/stg_<source>__<entity>.sql` | <purpose> |
| `models/staging/<source>/_<source>__sources.yml` | source declarations |
| `models/staging/<source>/_<source>__models.yml` | staging schema + tests |

## Files to modify

| Path | Change |
|---|---|
| <path> | <one-line change description> |

## Files to delete

<Empty unless the change removes models. List explicitly — silent deletes are a Constitution §11 violation.>

| Path | Reason |
|---|---|
| <path> | <why this is safe to remove> |

## Tests

<List the tests this plan will produce. Reference each AC.>

| Test | AC covered |
|---|---|
| `unique` and `not_null` on `stg_<source>__<entity>.<grain>` | AC2 |
| Unit test: <scenario> | AC3 |

## Risks

<Warehouse-agnostic risks. Warehouse-specific risks go in the warehouse section below.>

| Risk | Mitigation |
|---|---|
| <risk> | <mitigation> |

## Downstream impact

| Consumer | Impact | Notification |
|---|---|---|
| Semantic-layer metric `<metric>` | <none|breaking|additive> | <who/when> |
| Exposure `<exposure>` | <none|breaking|additive> | <who/when> |
| Reverse-ETL `<destination>` | <none|breaking|additive> | <who/when> |

## Open questions for review

- [ ] <question for the human reviewer>
