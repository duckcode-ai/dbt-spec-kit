# Tutorial 2: Ship a jaffle-shop change

This tutorial uses the upstream dbt Labs
[jaffle-shop](https://github.com/dbt-labs/jaffle-shop) project to show the full AI SDLC loop on a
real dbt repo.

For the longer narrative version, see the
[jaffle-shop AI SDLC walkthrough](../jaffle-shop-ai-sdlc-walkthrough.md).

## 1. Clone the example project

```bash
git clone https://github.com/dbt-labs/jaffle-shop.git
cd jaffle-shop
```

Set up jaffle-shop using its upstream instructions. At minimum, install dependencies and confirm dbt
can parse or build in your environment:

```bash
dbt deps
dbt parse
```

## 2. Add dbt-spec-kit

Use the warehouse preset that matches your local profile. BigQuery is shown here because many teams
use jaffle-shop for BigQuery demos:

```bash
uvx --from dbt-spec-kit dbt-specify init jaffle-shop --warehouse bigquery
dbt-specify doctor
```

## 3. Start from a business request

Ask your agent:

```text
/dbt.specify Add a customer segmentation field to the customers mart without breaking existing metrics.
```

The spec reviewer should check:

- the `customers` mart remains one row per customer
- existing metric names stay stable
- saved query references still resolve
- the segmentation logic has tests or explicit review evidence

## 4. Approve the plan before code

After the spec is approved:

```text
/dbt.plan
```

The plan should name the files the agent may edit, such as:

```text
models/marts/customers.sql
models/marts/customers.yml
```

If the agent proposes broad cleanup or unrelated refactors, reject the plan and ask it to narrow the
file list.

## 5. Break the work into tasks

```text
/dbt.tasks
```

Good tasks are small:

```text
- [ ] T1 Add customer_segment logic to customers.sql. AC: AC1, AC2, AC3, AC4.
- [ ] T2 Add tests and docs for customer_segment. AC: AC1, AC3, AC4.
- [ ] T3 Run parse and report evidence. AC: AC5.
```

The implementation agent should complete one checked task and stop.

For a short demo with a reviewed plan, you can use:

```text
/dbt.implement-all
```

It still runs tasks sequentially and stops if validation fails or the file scope changes.

## 6. Validate and review

Run:

```bash
dbt-specify validate project
dbt parse
dbt-specify validate dbt --manifest target/manifest.json
dbt-specify report --format markdown
```

Then ask:

```text
/dbt.review
```

The review should compare the final diff to the approved spec, plan, tasks, and command evidence.

## Success criteria

- The change starts as a business request.
- The approved plan owns the file list.
- The agent implements one task at a time.
- Review evidence includes dbt-spec-kit checks plus dbt parse or build output.
