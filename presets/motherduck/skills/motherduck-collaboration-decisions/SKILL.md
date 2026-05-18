---
name: motherduck-collaboration-decisions
description: Use when planning MotherDuck dbt work involving local/cloud execution, sharing, collaborators, files, and sensitive data movement.
---

# MotherDuck collaboration decisions

## When to use this skill

Use this for MotherDuck-backed dbt projects, shared analytics databases, or local-to-cloud DuckDB
workflows.

## Decision routine

1. Decide whether each model runs locally, in MotherDuck, or in a hybrid path.
2. List data that crosses local/cloud boundaries.
3. Document databases, shares, roles, and collaborators.
4. Confirm file/object-store sources are reproducible in CI and production.
5. Estimate large scans/exports and quota risk.
6. Block sensitive data synchronization without an approved handling decision.

## Common failures

- Treating local files as if every collaborator can access them.
- Sharing a database before role/access review.
- Moving PII between local and cloud execution without approval.
- Ignoring quota/cost impact for large exploratory scans.
