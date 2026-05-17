# Plan — Jaffle Shop staging layer overhaul

**Spec:** ./spec.md
**Author:** AI agent (proposed) + senior eng (approved)
**Date:** 2026-05-17
**Status:** approved

## Architecture

Replace three legacy staging models with three new ones following the 5-CTE pattern (Constitution Articles §9, §10). Old files are deleted (not deprecated) per the resolved open question in the spec. Downstream marts are updated to reference the new model names; this is a coordinated change to maintain Constitution §11 ("no silent breaking changes").

## Files to add

| Path | Purpose |
|---|---|
| `models/staging/jaffle_shop/stg_jaffle_shop__customers.sql` | 5-CTE pattern, surrogate key |
| `models/staging/jaffle_shop/stg_jaffle_shop__orders.sql` | 5-CTE pattern, surrogate key |
| `models/staging/jaffle_shop/stg_jaffle_shop__payments.sql` | 5-CTE pattern, surrogate key |
| `models/staging/jaffle_shop/_jaffle_shop__sources.yml` | source declarations with freshness |
| `models/staging/jaffle_shop/_jaffle_shop__models.yml` | schema tests + docs |
| `tests/unit/test_stg_jaffle_shop__customers_excludes_test_rows.sql` | unit test for AC6 |
| `tests/unit/test_stg_jaffle_shop__orders_preserves_row_count.sql` | unit test for AC7 |

## Files to modify

| Path | Change |
|---|---|
| `models/marts/dim_customers.sql` | update `ref('stg__customers')` → `ref('stg_jaffle_shop__customers')` |
| `models/marts/fct_orders.sql` | update `ref('stg__orders')` → `ref('stg_jaffle_shop__orders')` |
| `models/marts/fct_payments.sql` | update `ref('stg__payments')` → `ref('stg_jaffle_shop__payments')` |
| `models/marts/_marts.yml` | no change needed; sk references go through the new staging models |

## Files to delete

| Path | Reason |
|---|---|
| `models/staging/jaffle_shop/stg__customers.sql` | replaced by new naming |
| `models/staging/jaffle_shop/stg__orders.sql` | replaced |
| `models/staging/jaffle_shop/stg__payments.sql` | replaced |

## Tests

| Test | AC covered |
|---|---|
| `unique` and `not_null` on `customer_sk`, `order_sk`, `payment_sk` | AC4 |
| Unit test: `stg_jaffle_shop__customers` excludes `is_test = true` rows | AC6 |
| Unit test: `stg_jaffle_shop__orders` row count = source row count - test row count | AC7 |
| `dbt parse` after delete of old models | AC5 |

## Risks

| Risk | Mitigation |
|---|---|
| Mart refs miss one of the old staging models, causing parse failure | Run `dbt parse` after each task; CI catches it in the worst case |
| Surrogate key generation introduces row mismatches if source columns are NULL | Unit test on row count (AC7) catches it; also `not_null` test catches it |
| Existing CI uses old staging names | Grep CI configs; updated in T-08 |

## Downstream impact

| Consumer | Impact | Notification |
|---|---|---|
| Semantic-layer metric `total_orders` | none (uses `fct_orders.order_id`, unchanged) | n/a |
| Exposure `weekly_revenue_dashboard` | none (downstream of `fct_orders`) | n/a |
| Reverse-ETL `hubspot_customer_sync` | additive: gains `customer_sk` column, no change to existing | confirmed with marketing-ops in Slack |

## Open questions for review

- [x] Drop old files immediately vs. deprecate? — resolved in spec
- [x] Snowflake clustering on these? — no, all <1 GB

<!-- BEGIN SNOWFLAKE PLAN ADDITIONS (auto-appended by dbt-specify) -->

## Snowflake-specific concerns

### Clustering decisions

| Model | Size estimate | Clustering key | Justification |
|---|---|---|---|
| stg_jaffle_shop__customers | <100 MB | none | small, view materialization, clustering N/A |
| stg_jaffle_shop__orders | <500 MB | none | below 1 GB threshold |
| stg_jaffle_shop__payments | <100 MB | none | below 1 GB threshold |

### Warehouse sizing

| Job | Warehouse | Size | Auto-suspend (s) | Justification |
|---|---|---|---|---|
| daily dbt build | `transform_wh` | X-Small | 60 | views only; no compute cost |

### Query tag plan

`project=jaffle_shop, model=stg_jaffle_shop__<entity>, env=<env>, run_id=<run_id>`

### Masking & governance

| Column | Source | Policy | Tested? |
|---|---|---|---|
| `email` | `raw.jaffle_shop.customers.email` | `mask_email` | yes (existing) |

### Cost guardrails

| Risk | Mitigation |
|---|---|
| view evaluation cost on dashboard hits | acceptable — views materialize on-read, downstream marts are tables |

<!-- END SNOWFLAKE PLAN ADDITIONS -->
