# Enterprise customer 360 mart

**Ticket:** ENT-101
**Author:** Example
**Date:** 2026-05-18
**Status:** approved

## Problem

Customer reporting is split across CRM, billing, and product-event marts. Revenue, lifecycle, and
activation metrics disagree because each downstream team defines "customer" differently.

## Users

| User | Job to be done |
|---|---|
| Data platform lead | "I want one governed customer mart that teams can build metrics on without redefining grain." |
| RevOps analyst | "I want CRM and billing identifiers reconciled so account reporting is stable." |
| Product analytics lead | "I want activation fields joined without exposing raw PII." |

## What this is

Create a governed `dim_customers` mart with one row per canonical customer. The mart reconciles CRM,
billing, and product identifiers, preserves the existing semantic-layer metric inputs, and documents
all PII governance decisions.

## Acceptance criteria

- AC1: The system shall produce `dim_customers` with one row per canonical customer.
- AC2: The system shall expose CRM, billing, and product identifiers as documented columns.
- AC3: When duplicate CRM accounts map to one billing account, the system shall select the active account as canonical.
- AC4: If an email column is included, then the system shall apply the approved PII policy.
- AC5: Where semantic-layer metrics consume customer attributes, the system shall preserve existing metric names and dimensions.
- AC6: The system shall add source freshness checks for CRM, billing, and product-event sources.
- AC7: The system shall add tests proving unique grain, non-null canonical key, and duplicate-resolution behavior.

## Out of scope

- Rebuilding revenue facts
- Changing metric definitions
- Backfilling deleted customers before the current retention window

## Constraints

- Warehouse: Snowflake
- Materialization: table
- Grain: one row per canonical customer
- Refresh cadence: daily
- Downstream consumers: customer health dashboard, revenue semantic metrics, Salesforce reverse-ETL

## Open questions

- [x] Should inactive duplicate CRM accounts be retained? — yes, retain as non-canonical lineage columns.
