# Enterprise CI

dbt-spec-kit treats CI as the trust boundary for AI-assisted dbt work. Agents can draft and
implement, but CI proves that the work still follows the approved spec, plan, tasks, and dbt project
guardrails.

## Recommended PR checks

```bash
dbt-specify validate project
dbt parse
dbt-specify validate dbt --manifest target/manifest.json
dbt-specify report --format markdown > dbt-specify-report.md
```

Use `dbt-specify ci` when you want one release-blocking command that combines lifecycle and dbt
artifact checks.

## What gets checked

`validate project` checks the dbt-spec-kit lifecycle:

- `plan.md` does not exist before `spec.md` is approved.
- `tasks.md` does not exist before `plan.md` is approved.
- Acceptance criteria are EARS-formatted.
- Plans include required implementation sections.
- Plans and tasks reference the spec's AC ids.

`validate dbt` checks the dbt project and manifest:

- `dbt_project.yml` exists.
- model nodes have descriptions.
- model nodes have test children in the manifest.
- mart models named `dim_*` or `fct_*` declare grain.
- sources with freshness include loaded-at metadata.
- missing exposures are called out as adoption guidance.

## GitHub Actions example

See `.dbt-specify/templates/ci/github-actions-dbt-specify.yml` after running init, or
`templates/ci/github-actions-dbt-specify.yml` in this repo, for a reusable starting point. The
workflow assumes your dbt adapter and dbt profile are already available through your CI setup.

## PR evidence example

For the jaffle-shop semantic mart walkthrough, the PR should include:

- approved `specs/001-customer-segmentation/spec.md`
- approved `plan.md` and `tasks.md`
- `dbt parse` evidence showing semantic models, metrics, and saved queries still resolve
- `dbt-specify-report.md` generated with `dbt-specify report --format markdown`
- reviewer sign-off for metric compatibility and downstream impact
