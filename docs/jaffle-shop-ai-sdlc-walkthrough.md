# Jaffle-shop AI SDLC walkthrough

This walkthrough shows how a team can introduce dbt-spec-kit to the upstream
[dbt Labs jaffle-shop](https://github.com/dbt-labs/jaffle-shop) project without changing the demo
repo's dbt models first.

The goal is to make the AI SDLC concrete:

```text
idea -> spec.md -> plan.md -> tasks.md -> dbt implementation -> CI report -> review
```

## Why jaffle-shop works for this demo

The upstream project is small enough to understand quickly, but rich enough to show enterprise
concerns:

- staging models under `models/staging`
- marts under `models/marts`
- source declarations in `models/staging/__sources.yml`
- data tests and unit tests in mart YAML files
- semantic models, metrics, and saved queries in `models/marts/customers.yml` and
  `models/marts/orders.yml`
- dbt packages such as `dbt_utils`

That makes it a better demo than a toy SQL file because a change can affect tests, semantic metrics,
saved queries, and downstream review.

## 1. Prepare jaffle-shop

Use a fork or local clone of the upstream repo:

```bash
git clone https://github.com/dbt-labs/jaffle-shop.git
cd jaffle-shop
```

Set up jaffle-shop with dbt Cloud or dbt Core using the upstream README. At minimum, the project
needs dependencies installed and a working profile for your warehouse:

```bash
dbt deps
dbt seed --full-refresh --vars '{"load_source_data": true}'
dbt build
```

If you are using dbt Cloud, run the equivalent steps in the Cloud IDE or Cloud CLI.

## 2. Add dbt-spec-kit

Choose the preset that matches your warehouse:

```bash
uvx --from dbt-spec-kit dbt-specify init jaffle-shop --warehouse bigquery
```

For Snowflake, Databricks, or Trino, replace `bigquery` with the matching preset.

Run the brownfield diagnostic:

```bash
uvx --from dbt-spec-kit dbt-specify doctor
```

Expected result: doctor reports adoption status for `.dbt-specify/`, `.dbt-specify/agents/`,
`CLAUDE.md`, `specs/`, model inventory, and `target/manifest.json`. This is a readiness check, not
a dbt model change.

## 3. Demo story: semantic customer segmentation

Use this feature request with your AI agent:

```text
/dbt.specify Add a customer segmentation field to the customers mart without breaking existing metrics.
```

The spec should be created at:

```text
specs/001-customer-segmentation/spec.md
```

The human reviewer should confirm:

- grain stays one row per customer
- existing `customers` semantic model remains compatible
- existing metrics such as `lifetime_spend_pretax`, `count_lifetime_orders`, and
  `average_order_value` are not renamed
- saved query `customer_order_metrics` still resolves
- tests cover the new segmentation logic

Example acceptance criteria:

- AC1: The system shall add a `customer_segment` column to the `customers` mart.
- AC2: The system shall preserve the `customers` mart grain as one row per customer.
- AC3: When a customer has lifetime spend above the approved threshold, the system shall classify the customer into the high-value segment.
- AC4: If a customer has no orders, then the system shall classify the customer into the prospect segment.
- AC5: Where existing semantic metrics consume the `customers` mart, the system shall preserve metric names, entities, and saved query references.

## 4. Plan and tasks

After the spec is approved:

```text
/dbt.plan
/dbt.tasks
```

The plan should explicitly mention jaffle-shop files such as:

- `models/marts/customers.sql`
- `models/marts/customers.yml`
- `models/marts/orders.yml`, only if the metric or saved query impact requires it

The plan should map every acceptance criterion to tests or validation evidence. For this demo, the
expected evidence is:

- schema tests still pass on `customer_id`
- unit or data test covers segment assignment
- `dbt parse` confirms semantic model, metric, and saved query references
- `dbt-specify validate project` confirms AC traceability

## 5. Implement one task at a time

Implementation stays bounded:

```text
/dbt.implement
```

After each task, the agent should run the task's validation command and stop. It should not jump
ahead to unrelated model cleanup.

Before review, run:

```bash
uvx --from dbt-spec-kit dbt-specify validate project
dbt parse
uvx --from dbt-spec-kit dbt-specify validate dbt --manifest target/manifest.json
uvx --from dbt-spec-kit dbt-specify report --format markdown > dbt-specify-report.md
```

If you installed with `uv tool install dbt-spec-kit`, the direct `dbt-specify` command is equivalent.

Then ask the agent:

```text
/dbt.review
```

The review should answer:

- Did the final diff match the approved plan?
- Which ACs were validated?
- Which dbt tests and parse checks passed?
- Did semantic models, metrics, and saved queries remain compatible?
- Are any downstream consumers or reviewers still needed?

## 6. What to show in a team demo

Use this 20-minute flow:

| Minute | What to show |
|---|---|
| 0-3 | Explain why raw AI prompts drift on dbt work |
| 3-6 | Show jaffle-shop's `customers` mart and semantic YAML |
| 6-10 | Show the approved `spec.md` and EARS acceptance criteria |
| 10-14 | Show `plan.md` mapping files and tests to ACs |
| 14-17 | Show `tasks.md` and one-task-at-a-time implementation |
| 17-20 | Show `dbt-specify-report.md` as PR evidence |

The message to the team: AI can help move faster, but the contract is still spec, plan, tests, and
human review.
