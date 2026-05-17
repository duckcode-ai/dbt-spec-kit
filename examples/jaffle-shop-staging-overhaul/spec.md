# Jaffle Shop staging layer overhaul

**Ticket:** EX-001
**Author:** Example
**Date:** 2026-05-17
**Status:** approved

## Problem

The jaffle-shop staging models predate our current conventions. They don't follow the 5-CTE pattern, don't generate surrogate keys, and have inconsistent naming (some files use `stg__orders.sql`, others `stg_orders.sql`). New analytics engineers see them and either copy the wrong patterns or get confused about which is canonical.

## Users

| User | Job to be done |
|---|---|
| Analytics engineer joining the team | "I want to see one consistent staging pattern across all sources so I can ship my first model without guessing." |
| Senior analytics engineer reviewing PRs | "I want to stop manually pointing out the same staging-convention issues on every review." |

## What this is

Rewrite the jaffle-shop source's staging models (`stg_jaffle_shop__customers`, `stg_jaffle_shop__orders`, `stg_jaffle_shop__payments`) to follow the project's current 5-CTE pattern, with surrogate keys, explicit type casts, and consistent naming. No business-logic changes — same rows in, same rows out.

## Acceptance criteria

- AC1: The system shall produce three staging models named `stg_jaffle_shop__customers`, `stg_jaffle_shop__orders`, `stg_jaffle_shop__payments`.
- AC2: The system shall use the 5-CTE pattern (source → renamed → filtered → enhanced → final) in each staging model.
- AC3: The system shall generate a surrogate key column named `<entity>_sk` via `dbt_utils.generate_surrogate_key`.
- AC4: The system shall enforce `unique` and `not_null` on each surrogate key.
- AC5: When a downstream mart references the old staging model name, the system shall fail at parse time with a clear error.
- AC6: If a source row has `is_test = true`, then the system shall exclude it from the staging output.
- AC7: The system shall preserve the same row count (minus test rows) compared to the previous staging output, verified by a unit test fixture.

## Out of scope

- Adding new columns (we're refactoring, not extending)
- Modifying any intermediate or mart model
- Changing the jaffle-shop seed data
- Snowflake clustering (none of these tables exceed 1 GB)

## Constraints

- Warehouse: Snowflake
- Materialization: view (staging models stay as views)
- Grain: one row per source entity (orders/customers/payments), unchanged
- Refresh cadence: same as source (daily)
- Downstream consumers: `dim_customers`, `fct_orders`, `fct_payments` — all need to point at the new staging names

## Open questions

- [x] Drop the old `stg__orders.sql` (double underscore) immediately or keep as deprecated for one release? — **resolved: drop immediately, this is internal**
