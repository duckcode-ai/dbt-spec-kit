---
name: reviewing-pii-access-governance
description: Use when reviewing dbt specs, plans, or diffs that touch PII, access, grants, contracts, exposures, or governed data products.
---

# Reviewing PII, access, and governance

## When to use this skill

Use this for any source, model, seed, snapshot, metric, or exposure that includes personal data,
financial data, regulated fields, access policy changes, or cross-team data products.

## Review routine

1. Identify sensitive columns and classify them as PII, financial, contractual, operational, or public.
2. Check that masking, policy tags, grants, row filters, or authorized views are declared in the plan.
3. Confirm model contracts preserve stable names and types for governed outputs.
4. Confirm owners and downstream consumers are listed for marts, metrics, and exposures.
5. Confirm retention, deletion, and late-arriving-data policies are explicit when relevant.
6. Block implementation if sensitive data appears in a new mart without an access decision.

## Required evidence

- Sensitive fields inventory.
- Access or masking decision.
- Contract impact statement.
- Owner and reviewer sign-off for governed outputs.

## Common failures

- Masking in marts instead of the staging boundary.
- Creating a convenience mart with unrestricted PII.
- Changing a semantic-layer field without naming downstream consumers.
