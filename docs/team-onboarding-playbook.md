# Team onboarding playbook

This playbook is for data platform leads introducing dbt-spec-kit to an analytics engineering team.

## Day 0: align on the workflow

Start with the operating model:

```text
idea -> spec -> plan -> tasks -> implementation -> review -> retro
```

Roles:

| Role | Responsibility |
|---|---|
| Data platform lead | Owns the constitution, CI policy, and warehouse preset |
| Analytics engineer | Reviews specs, plans, tasks, and final dbt diffs |
| AI agent | Drafts artifacts and implements approved tasks |
| Reviewer | Confirms ACs, tests, downstream impact, and governance |

Team rules:

- no implementation before spec approval
- no implementation outside the approved plan
- one task per implementation pass by default
- CI evidence is part of the PR
- retros update team context instead of relying on memory

## Week 1: adopt without disrupting production

1. Pick one non-emergency feature.
2. Run `dbt-specify doctor` on the repo.
3. Run `dbt-specify init <project> --warehouse <warehouse>`.
4. Merge the generated agent context into the repo.
5. Use `/dbt.specify`, `/dbt.plan`, and `/dbt.tasks` before any code change.
6. Attach `dbt-specify report --format markdown` output to the PR.

Keep CI warning-first for the first few PRs. Promote `dbt-specify ci` to a required check once the
team agrees on conventions and false positives are fixed.

## First production PR

The first production PR should be small but meaningful. Good candidates:

- add a documented mart column
- add or repair source freshness
- add a unit test around existing business logic
- update a semantic metric without renaming existing metrics

Avoid:

- full repo rewrites
- warehouse migrations
- large naming-standard refactors
- multiple domains in one PR

## Presentation agenda

Use this agenda for a team rollout meeting:

| Time | Topic |
|---|---|
| 5 min | Why AI agents need dbt-specific guardrails |
| 10 min | Walk through jaffle-shop spec, plan, tasks, and report |
| 10 min | Show how CI blocks drift from the approved plan |
| 10 min | Decide team approval rules and first pilot PR |
| 5 min | Capture open questions and ownership |

## Adoption checklist

- [ ] Warehouse preset chosen
- [ ] `.dbt-specify/constitution.md` reviewed
- [ ] `CLAUDE.md` merged or reconciled
- [ ] First spec approved by a human reviewer
- [ ] First plan approved before implementation
- [ ] `dbt-specify report` attached to first PR
- [ ] Retros used to improve team context
- [ ] `dbt-specify ci` promoted when the team is ready
