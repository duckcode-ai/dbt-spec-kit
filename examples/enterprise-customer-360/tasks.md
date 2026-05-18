# Tasks — Enterprise customer 360 mart

**Plan:** ./plan.md
**Status:** approved

## Task list

- [ ] **T-01** — Add CRM, billing, and product source declarations with freshness.
  - **Done when:** `dbt source freshness` runs for the three sources.
  - **Validates:** AC6

- [ ] **T-02** — Build `int_customer_identity_resolution` with canonical duplicate selection.
  - **Done when:** `dbt build --select int_customer_identity_resolution` runs green.
  - **Validates:** AC2, AC3

- [ ] **T-03** — Add unit test for duplicate CRM account resolution.
  - **Done when:** The test fails without active-account preference and passes with it.
  - **Validates:** AC3, AC7

- [ ] **T-04** — Build `dim_customers` with canonical grain and governed email.
  - **Done when:** `dbt build --select dim_customers` runs green.
  - **Validates:** AC1, AC2, AC4, AC5

- [ ] **T-05** — Add mart docs, grain declaration, and schema tests.
  - **Done when:** `dbt test --select dim_customers` runs green.
  - **Validates:** AC1, AC2, AC7

- [ ] **T-06** — Confirm semantic metric and exposure dependencies.
  - **Done when:** `dbt parse` resolves semantic and exposure references.
  - **Validates:** AC5

## Test plan

- [ ] `dbt-specify validate project` passes
- [ ] `dbt parse` succeeds
- [ ] `dbt-specify validate dbt --manifest target/manifest.json` passes
- [ ] `dbt build --select +dim_customers+` runs green
- [ ] Unit test for duplicate resolution is present and green

## Done definition

- [ ] All tasks above are checked
- [ ] All ACs are verified
- [ ] Downstream-impact actions are complete
- [ ] CI report is attached to the PR
