# Tasks — Jaffle Shop staging layer overhaul

**Plan:** ./plan.md
**Status:** done

## Task list

- [x] **T-01** — Create `_jaffle_shop__sources.yml` with freshness and loaded-at fields for customers, orders, payments.
  - **Done when:** `dbt parse` succeeds and `dbt source freshness` runs against the sources.
  - **Validates:** AC1 (precondition)

- [x] **T-02** — Create `stg_jaffle_shop__customers.sql` using the 5-CTE pattern, with `customer_sk` via `dbt_utils.generate_surrogate_key`.
  - **Done when:** `dbt build --select stg_jaffle_shop__customers` runs green.
  - **Validates:** AC1, AC2, AC3

- [x] **T-03** — Create `stg_jaffle_shop__orders.sql` (same pattern).
  - **Done when:** `dbt build --select stg_jaffle_shop__orders` runs green.
  - **Validates:** AC1, AC2, AC3

- [x] **T-04** — Create `stg_jaffle_shop__payments.sql` (same pattern).
  - **Done when:** `dbt build --select stg_jaffle_shop__payments` runs green.
  - **Validates:** AC1, AC2, AC3

- [x] **T-05** — Create `_jaffle_shop__models.yml` with `unique` + `not_null` tests on each surrogate key.
  - **Done when:** `dbt test --select staging.jaffle_shop` runs green.
  - **Validates:** AC4

- [x] **T-06** — Create unit test `test_stg_jaffle_shop__customers_excludes_test_rows.sql`.
  - **Done when:** Test runs and fails when test-row filter is removed; passes when filter is present.
  - **Validates:** AC6

- [x] **T-07** — Create unit test `test_stg_jaffle_shop__orders_preserves_row_count.sql`.
  - **Done when:** Test passes against the fixture.
  - **Validates:** AC7

- [x] **T-08** — Update `dim_customers`, `fct_orders`, `fct_payments` mart refs to point at new staging model names.
  - **Done when:** `dbt parse` succeeds; `dbt build --select +dim_customers+ +fct_orders+ +fct_payments+` runs green.
  - **Validates:** AC5 (precondition — old refs would fail)

- [x] **T-09** — Delete `stg__customers.sql`, `stg__orders.sql`, `stg__payments.sql`.
  - **Done when:** `dbt parse` succeeds after deletion (proves AC5: no remaining ref to old names).
  - **Validates:** AC5

## Test plan

- [x] `dbt build --select +fct_orders+` runs green locally on a fresh schema
- [x] `dbt test` passes for all changed models
- [x] Unit tests for AC6 and AC7 are present and green
- [x] `weekly_revenue_dashboard` exposure still resolves

## Done definition

- [x] All tasks above are checked
- [x] All ACs are verified
- [x] Plan's downstream-impact actions completed (no external notifications needed for this refactor)
- [x] Retro filed (see `implementation-summary.md`)
