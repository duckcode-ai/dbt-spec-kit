# Confluence integration

The Confluence bridge lets teams use wiki pages as approved business and architecture context
without turning the wiki into the source of truth for dbt implementation.

```text
Confluence context -> local context markdown -> spec.md -> plan.md -> Confluence summary page
```

Confluence is for shared knowledge. The local `spec.md`, `plan.md`, and `tasks.md` files remain the
implementation contract.

## Authentication

Set these environment variables before running Confluence commands:

```bash
export CONFLUENCE_BASE_URL="https://your-company.atlassian.net"
export CONFLUENCE_EMAIL="you@company.com"
export CONFLUENCE_API_TOKEN="<atlassian-api-token>"
```

Create the token from [Atlassian account security settings](https://id.atlassian.com/manage-profile/security/api-tokens)
and make sure the account can read, create, and update pages in the target space. The bridge uses
the [Confluence Cloud REST API v2 page endpoints](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/).
Do not commit these values. Use local shell secrets or CI secrets.

## Pull a wiki page into spec context

Run from the dbt project root:

```bash
uvx --from dbt-spec-kit dbt-specify confluence pull-page 123456789 \
  --to specs/001-player-journey/context/player-metrics.md
```

This creates or updates:

```text
specs/001-player-journey/
  confluence.yml
  context/
    player-metrics.md
```

The context file contains the page title, URL, page id, sync timestamp, and a lightweight markdown
rendering of the page body. `confluence.yml` records the source page so reviewers know where the
context came from.

Use this for focused wiki context only. Do not bulk-copy entire spaces into the repo.

## Publish a spec summary page

After `spec.md` and `plan.md` are approved:

```bash
uvx --from dbt-spec-kit dbt-specify confluence publish \
  --spec-dir specs/001-player-journey \
  --space-key DATA \
  --parent-id 987654321
```

This creates a Confluence page summarizing the local artifacts and writes page metadata to
`specs/001-player-journey/confluence.yml`.

If your automation already knows the Confluence v2 space id, use `--space-id` instead of
`--space-key`:

```bash
uvx --from dbt-spec-kit dbt-specify confluence publish \
  --spec-dir specs/001-player-journey \
  --space-id 12345
```

To update an existing page:

```bash
uvx --from dbt-spec-kit dbt-specify confluence publish \
  --spec-dir specs/001-player-journey \
  --page-id 123456789
```

Preview without writing:

```bash
uvx --from dbt-spec-kit dbt-specify confluence publish \
  --spec-dir specs/001-player-journey \
  --space-key DATA \
  --dry-run
```

Dry-run reads local files only and does not require Confluence credentials.

## Sync a previously published page

Once `confluence.yml` has a `page_id`, use:

```bash
uvx --from dbt-spec-kit dbt-specify confluence sync \
  --spec-dir specs/001-player-journey
```

This updates the recorded page from current local files.

## What gets published

The summary page includes the available files from the spec directory:

- `spec.md`
- `plan.md`
- `tasks.md`
- `review.md`
- `governance-review.md`
- `dbt-specify-report.md`
- markdown files under `context/`

The page is intentionally a readable knowledge summary. It does not replace the PR, CI checks, or
the local approved artifacts.

## Recommended enterprise policy

- Pull only relevant Confluence pages into `specs/<NNN>/context/`.
- Keep page ids and URLs in `confluence.yml` for traceability.
- Publish only approved or review-ready spec directories.
- Use Confluence for durable business summaries, onboarding, architecture notes, and metric
  definitions.
- Keep Jira as the ticket/task tracker and the PR as the merge gate.
- Use `confluence publish --dry-run` before the first production rollout.

## Troubleshooting

- `Missing Confluence environment variable`: set `CONFLUENCE_BASE_URL`, `CONFLUENCE_EMAIL`, and
  `CONFLUENCE_API_TOKEN`.
- `Confluence space not found`: verify `--space-key` or pass `--space-id`.
- `confluence.yml is missing page_id`: run `confluence publish` before `confluence sync`.
- `HTTP 401`: check the email/token pair and site URL.
- `HTTP 403`: confirm the account can read pages and create or update pages in the target space.
