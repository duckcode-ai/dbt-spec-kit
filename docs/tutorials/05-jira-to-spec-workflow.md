# Tutorial 5: Jira to spec workflow

This tutorial shows the enterprise intake path: start from a Jira story, generate a local
dbt-spec-kit spec, approve the plan, and publish approved artifacts back to Jira.

## 1. Configure Jira credentials

```bash
export JIRA_BASE_URL="https://your-company.atlassian.net"
export JIRA_EMAIL="you@company.com"
export JIRA_API_TOKEN="<atlassian-api-token>"
```

Use a local shell profile or secret manager. Do not write tokens into the repo.

## 2. Pull the Jira issue

Run from the dbt project root:

```bash
uvx --from dbt-spec-kit dbt-specify jira pull NBA-123
```

Expected output:

```text
created specs/001-nba-123-player-journey/spec.md
created specs/001-nba-123-player-journey/jira.yml
```

Review `spec.md`. The generated file is a draft from Jira context, not an approved contract.

## 3. Refine the spec with an agent

Ask your agent:

```text
Read specs/001-nba-123-player-journey/spec.md and the current dbt project.
Refine the spec into clear business meaning, grain, downstream consumers, and EARS acceptance
criteria. Do not edit SQL or YAML models.
```

Approve `spec.md` before moving on.

## 4. Plan and tasks

Use the normal workflow:

```text
/dbt.plan
/dbt.tasks
```

Approve `plan.md` before implementation. Approve `tasks.md` before creating Jira subtasks.

## 5. Attach spec and plan to Jira

```bash
uvx --from dbt-spec-kit dbt-specify jira attach NBA-123 \
  --spec specs/001-nba-123-player-journey/spec.md \
  --plan specs/001-nba-123-player-journey/plan.md
```

## 6. Create Jira subtasks

```bash
uvx --from dbt-spec-kit dbt-specify jira create-tasks NBA-123 \
  --from specs/001-nba-123-player-journey/tasks.md
```

For a first rollout, preview first:

```bash
uvx --from dbt-spec-kit dbt-specify jira create-tasks NBA-123 \
  --from specs/001-nba-123-player-journey/tasks.md \
  --dry-run
```

## 7. Implement and review

Implementation remains local and PR-driven:

```text
/dbt.implement
/dbt.review
```

After validation, attach final evidence if your team requires it:

```bash
uvx --from dbt-spec-kit dbt-specify report --format markdown > dbt-specify-report.md
uvx --from dbt-spec-kit dbt-specify jira attach NBA-123 --file dbt-specify-report.md
```

## Success criteria

- Jira story context is captured in `jira.yml` and `spec.md`.
- The approved spec and plan are attached to the Jira issue.
- Jira subtasks match `tasks.md` and do not duplicate on reruns.
- The PR remains the merge gate for dbt code.
