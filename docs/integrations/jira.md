# Jira integration

The Jira bridge lets enterprise teams keep Jira as the intake and tracking system while keeping
`spec.md`, `plan.md`, and `tasks.md` as the local engineering contract.

```text
Jira story -> spec.md -> plan.md -> tasks.md -> Jira attachments/subtasks -> PR evidence
```

Jira does not replace the dbt-spec-kit workflow. It provides source context and receives approved
artifacts after review.

## Authentication

Set these environment variables before running Jira commands:

```bash
export JIRA_BASE_URL="https://your-company.atlassian.net"
export JIRA_EMAIL="you@company.com"
export JIRA_API_TOKEN="<atlassian-api-token>"
```

Do not commit these values. Use local shell secrets or CI secrets.

## Pull a Jira story into a spec

Run from the dbt project root:

```bash
uvx --from dbt-spec-kit dbt-specify jira pull NBA-123
```

This creates:

```text
specs/001-nba-123-player-journey/
  jira.yml
  spec.md
```

`jira.yml` records the Jira issue key, URL, project key, local spec directory, and last sync time.
`spec.md` is a draft. A human or AI agent should refine the business meaning, acceptance criteria,
grain, downstream consumers, and open questions before the plan phase.

## Plan and task locally

Use the normal agent workflow:

```text
/dbt.plan
/dbt.tasks
```

Review and approve `spec.md` before planning. Review and approve `plan.md` before implementation.

## Attach approved artifacts to Jira

Attach the approved spec and plan:

```bash
uvx --from dbt-spec-kit dbt-specify jira attach NBA-123 \
  --spec specs/001-nba-123-player-journey/spec.md \
  --plan specs/001-nba-123-player-journey/plan.md
```

The command uploads each file to the Jira issue and adds a short comment listing the attached
artifacts. Add `--no-comment` when an automation or PR comment already summarizes the evidence.

## Create Jira subtasks from tasks.md

After tasks are approved:

```bash
uvx --from dbt-spec-kit dbt-specify jira create-tasks NBA-123 \
  --from specs/001-nba-123-player-journey/tasks.md
```

Each unchecked task becomes a Jira subtask with a summary like:

```text
[dbt-specify T-01] Add player journey mart. AC: AC1, AC2.
```

The prefix keeps sync idempotent. If the command sees an existing child issue with the same
`[dbt-specify T-01]` prefix, it skips that task instead of creating a duplicate.

Use `--dry-run` to preview:

```bash
uvx --from dbt-spec-kit dbt-specify jira create-tasks NBA-123 \
  --from specs/001-nba-123-player-journey/tasks.md \
  --dry-run
```

If your Jira site uses a different subtask type name, pass it explicitly:

```bash
uvx --from dbt-spec-kit dbt-specify jira create-tasks NBA-123 \
  --from specs/001-nba-123-player-journey/tasks.md \
  --issue-type "Subtask"
```

## Sync a spec directory

For the common case, sync the directory:

```bash
uvx --from dbt-spec-kit dbt-specify jira sync NBA-123 \
  --spec-dir specs/001-nba-123-player-journey
```

This attaches `spec.md` and `plan.md` when they exist, then creates missing Jira subtasks from
`tasks.md`.

## Recommended enterprise policy

- Pull Jira context into a spec branch, not directly into `main`.
- Attach only reviewed or approved `spec.md` and `plan.md`; avoid publishing raw agent drafts.
- Create Jira subtasks after `tasks.md` is approved.
- Keep the PR as the merge gate. Jira status alone does not approve dbt code.
- Store Jira credentials in environment variables or CI secrets only.
- Use `jira sync --dry-run` before the first production rollout.

## Troubleshooting

- `Missing Jira environment variable`: set `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN`.
- `Jira API request failed with HTTP 401`: check the email/token pair and site URL.
- `Jira API request failed with HTTP 403`: confirm the account can browse the issue, add
  attachments, create issues, and create subtasks in the project.
- Duplicate subtasks: check whether existing child issues use the `[dbt-specify T-XX]` prefix.
