# Plan — Enterprise customer 360 mart

**Spec:** ./spec.md
**Author:** AI agent (proposed) + data platform lead (approved)
**Date:** 2026-05-18
**Status:** approved

## Architecture

Add source declarations for CRM, billing, and product events, then build staging models that normalize
identifiers before a single mart-level `dim_customers` table. Duplicate resolution is isolated in an
intermediate model so AC3 has deterministic unit-test coverage. PII policy handling and semantic-layer
impact are documented before implementation.

## Files to add

| Path | Purpose |
|---|---|
| `models/staging/crm/_crm__sources.yml` | CRM source freshness for AC6 |
| `models/staging/billing/_billing__sources.yml` | Billing source freshness for AC6 |
| `models/staging/product/_product__sources.yml` | Product-event source freshness for AC6 |
| `models/intermediate/customers/int_customer_identity_resolution.sql` | Duplicate resolution for AC2, AC3 |
| `models/marts/customers/dim_customers.sql` | Canonical customer mart for AC1, AC2, AC4, AC5 |
| `models/marts/customers/_customers__models.yml` | Docs, grain, and schema tests for AC1, AC2, AC4, AC7 |
| `tests/unit/test_customer_identity_resolution.sql` | Unit test for AC3 and AC7 |

## Files to modify

| Path | Change |
|---|---|
| `models/semantic/customer_metrics.yml` | Confirm existing metric names and dimensions for AC5 |
| `models/exposures/customer_health.yml` | Confirm downstream dashboard dependency for AC5 |
| `models/_governance/masking_policies.sql` | Reference approved email masking policy for AC4 |

## Files to delete

| Path | Reason |
|---|---|
| (none) | No existing mart is removed in this release |

## Tests

| Test | AC covered |
|---|---|
| `unique` and `not_null` on `dim_customers.customer_sk` | AC1, AC7 |
| Accepted source freshness checks for CRM, billing, product events | AC6 |
| Unit test: duplicate CRM accounts resolve to active canonical account | AC3, AC7 |
| Governance test: email masking policy applies to mart email column | AC4 |
| Semantic-layer parse after metric file confirmation | AC5 |
| Column docs include CRM, billing, and product identifiers | AC2 |

## Risks

| Risk | Mitigation |
|---|---|
| Identity-resolution logic changes revenue reporting | Keep revenue facts unchanged; validate semantic metric parse before merge |
| PII leaks through mart docs or unmasked email | Apply approved masking policy and test with deterministic fixture |

## Downstream impact

| Consumer | Impact | Notification |
|---|---|---|
| Semantic-layer metric `customer_count` | none; existing metric name preserved | data platform lead before merge |
| Exposure `customer_health_dashboard` | additive; new canonical fields available | dashboard owner in PR |
| Reverse-ETL `salesforce_customer_sync` | additive; canonical key added | RevOps approver in PR |

## Open questions for review

- [x] Should this replace existing revenue facts? — no, mart only.
- [x] Should raw email be included? — yes, masked by policy.

## Snowflake-specific concerns

### Clustering decisions

| Model | Size estimate | Clustering key | Justification |
|---|---|---|---|
| `dim_customers` | 3 GB | `[customer_sk]` | frequent customer lookup and reverse-ETL sync |

### Warehouse sizing

| Job | Warehouse | Size | Auto-suspend (s) | Justification |
|---|---|---|---|---|
| daily customer mart build | `transform_wh` | Small | 60 | identity resolution joins three governed sources |

### Query tag plan

`project=customer_360, model=<model>, env=<env>, run_id=<run_id>`

### Masking & governance

| Column | Source | Policy | Tested? |
|---|---|---|---|
| `email` | `crm.accounts.email` | `mask_email` | yes |

### Cost guardrails

| Risk | Mitigation |
|---|---|
| Full scan of product events | staging model filters to retained customer identity fields and daily active window |
