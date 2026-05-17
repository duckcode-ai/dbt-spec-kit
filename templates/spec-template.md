<!-- INSTRUCTIONS:
  Fill in every section below. Acceptance criteria MUST be in EARS format:
    - Ubiquitous:    "The system shall <response>."
    - Event-driven:  "When <trigger>, the system shall <response>."
    - State-driven:  "While <state>, the system shall <response>."
    - Unwanted:      "If <unwanted>, then the system shall <response>."
    - Optional:      "Where <feature>, the system shall <response>."
  Run `dbt-specify validate path/to/this/spec.md` to check EARS conformance.
  Remove this INSTRUCTIONS block before merging — or leave it; future iterations benefit.
-->

# <feature title>

**Ticket:** <project tracker id>
**Author:** <name>
**Date:** <YYYY-MM-DD>
**Status:** draft | approved | shipped

## Problem

<One paragraph. What's broken or missing. Who's affected. Why now.>

## Users

<Who this is for and the job they're hiring it for. One row per user type.>

| User | Job to be done |
|---|---|
| <persona> | <one-sentence job> |

## What this is

<2–4 sentences. The result of this work, in plain language. No tech stack details — those go in the plan.>

## Acceptance criteria

<!-- Each AC is one line. Each line uses an EARS pattern. -->

- AC1: <ubiquitous AC>
- AC2: <event-driven AC>
- AC3: <unwanted-condition AC>

## Out of scope

<What this does NOT do. Be specific — vague out-of-scope sections are common spec failure modes.>

- <thing we are not doing>
- <thing someone might assume but we are not doing>

## Constraints

- Warehouse: <snowflake|databricks|other>
- Materialization: <table|view|incremental|...>
- Grain: <one sentence — what is one row?>
- Refresh cadence: <hourly|daily|on-demand>
- Downstream consumers: <semantic layer metrics, dashboards, reverse-ETL, ML features>

## Open questions

<Things the spec doesn't decide yet. Resolve before plan phase.>

- [ ] <question>
