---
name: writing-business-glossary-specs
description: Use when writing a tier-3 spec that captures business domain context — entity definitions, grain decisions, cross-system identifier resolution.
---

# Writing business glossary specs

## When to use this skill

You're working on a data model where the *business meaning* of an entity isn't obvious from the source data. Examples:

- "Customer" means different things in Salesforce vs. Stripe vs. the product database.
- A "Well" is identified by EID across systems, but ProdView stores it as a Unit and ODA stores it as a Property — the grain is different and entity resolution is required.
- The marketing team's "session" and the product team's "session" have different boundaries.
- "Revenue" depends on whether you're talking GAAP-recognized, billed, or contracted.

This is the layer dbt-labs/dbt-agent-skills explicitly doesn't cover (see [dbt-core discussion #12521](https://github.com/dbt-labs/dbt-core/discussions/12521)) and where AI agents most often produce plausible-looking but business-wrong models.

## The three tiers (from the dbt-core discussion)

| Tier | Covers | Owner |
|---|---|---|
| 1 — Framework | "how to add a unit test", dbt mechanics | dbt-labs/dbt-agent-skills |
| 2 — Project | "our staging models use a 5-CTE pattern" | each project's CLAUDE.md |
| 3 — Business | "a Well is identified by EID across systems" | **this skill** |

## Template

```markdown
# Business glossary spec — <entity name>

## Definition

<One paragraph. What this entity IS in plain business language. Avoid technical jargon. If a non-technical stakeholder reads this, do they nod?>

## Canonical identifier

The canonical identifier for <entity> is `<column>`. All cross-system joins MUST resolve to this identifier.

## Source-system aliases

| System | Their name | Their identifier | Notes |
|---|---|---|---|
| Salesforce | `Account` | `Account.Id` (18-char) | also has 15-char `AccountId` — never use |
| Stripe | `Customer` | `Customer.id` | prefixed `cus_` |
| Internal product DB | `users.account_id` | `bigint` | |

## Entity resolution rules

<How do we resolve a record from System A to the canonical entity in System B? This is often non-trivial.>

1. Prefer match on `<external_id_field>` populated by the integration team.
2. Fall back to email-domain match for Salesforce ↔ product DB.
3. NEVER use name-similarity match.

## Grain decisions

When this entity appears in a model, the grain is one of:

- **point-in-time** (entity state as of timestamp T)
- **as-of-current** (latest known state)
- **event-sourced** (one row per change)

Specify which grain the model uses and why.

## Business rules

<The non-obvious rules a non-domain expert wouldn't know.>

- A customer with `is_test = true` is excluded from all financial reporting but included in product analytics.
- A customer is "active" if they had a billable event in the last 30 days, NOT if they have an active subscription record (legacy subscription records persist after churn).

## Common mistakes the AI agent must avoid

<Past errors that should not be repeated. This list grows over time.>

- Treating Salesforce's 15-char `Id` as canonical (it's not — the 18-char form is).
- Using `users.created_at` to compute customer tenure (use `accounts.signup_date` — `users.created_at` is the auth-system timestamp, not the customer's relationship start).
```

## Anti-patterns

- **Skipping this spec for "simple" entities** — even "user" has multiple definitions in most companies.
- **Writing the glossary spec inside the model spec** — the glossary outlives any single model; it's its own artifact.
- **Capturing business rules only in code comments** — they get lost in refactors.

## How to know this is working

Six months from now, a new analytics engineer joins the team and is asked to add a new mart that joins customer data across two source systems. They find this spec, follow the entity resolution rules, and produce a correct join on the first try without asking the original author. That's the bar.
