# Tutorial 6: Confluence context workflow

This tutorial shows how to use Confluence pages as approved business context for a dbt-spec-kit
feature, then publish the final spec summary back to Confluence.

## 1. Configure Confluence credentials

```bash
export CONFLUENCE_BASE_URL="https://your-company.atlassian.net"
export CONFLUENCE_EMAIL="you@company.com"
export CONFLUENCE_API_TOKEN="<atlassian-api-token>"
```

Use a local shell profile or secret manager. Do not write tokens into the repo.

## 2. Pull relevant wiki context

Run from the dbt project root:

```bash
uvx --from dbt-spec-kit dbt-specify confluence pull-page 123456789 \
  --to specs/001-player-journey/context/player-metrics.md
```

Expected output:

```text
pulled Player metric definitions (123456789)
wrote specs/001-player-journey/context/player-metrics.md
```

The spec directory also gets `confluence.yml` with source page traceability.

## 3. Ask the agent to use context carefully

Ask your agent:

```text
Read specs/001-player-journey/context/player-metrics.md and the current dbt project.
Use it as source context for business meaning, but keep the approved spec.md as the implementation
contract. Do not edit SQL or YAML yet.
```

Then run the normal workflow:

```text
/dbt.specify Build a player journey mart using the approved player metrics definitions.
/dbt.plan
/dbt.tasks
```

## 4. Publish the approved summary

After `spec.md` and `plan.md` are approved:

```bash
uvx --from dbt-spec-kit dbt-specify confluence publish \
  --spec-dir specs/001-player-journey \
  --space-key DATA \
  --parent-id 987654321
```

This creates a Confluence page and records the page id in:

```text
specs/001-player-journey/confluence.yml
```

## 5. Sync after review

After implementation and review evidence are added:

```bash
uvx --from dbt-spec-kit dbt-specify report --format markdown \
  > specs/001-player-journey/dbt-specify-report.md

uvx --from dbt-spec-kit dbt-specify confluence sync \
  --spec-dir specs/001-player-journey
```

## Success criteria

- Confluence source context is stored under `context/`, not copied blindly into the spec.
- `confluence.yml` records source page ids and the published summary page id.
- The Confluence summary reflects approved local artifacts.
- The PR remains the merge gate for dbt code.
