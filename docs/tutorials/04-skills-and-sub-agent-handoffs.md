# Tutorial 4: Run skills and sub-agent handoffs

This tutorial explains how to use skills and sub-agent templates without creating unsafe parallel
edits.

## 1. Install dbt framework skills separately

dbt-spec-kit does not copy dbt Labs skills. Install them separately and let your agent use them for
dbt framework mechanics.

Claude Code:

```text
/plugin marketplace add dbt-labs/dbt-agent-skills
/plugin install dbt@dbt-agent-marketplace
```

Vercel Skills CLI:

```bash
npx skills add dbt-labs/dbt-agent-skills
```

Tessl:

```bash
tessl install dbt-labs/dbt-agent-skills
```

## 2. Know what each layer owns

| Layer | Use for |
|---|---|
| dbt Labs skills | dbt commands, unit tests, semantic layer, Mesh, docs lookup, migrations |
| `CLAUDE.md` | local project conventions |
| `.dbt-specify/skills/` | business meaning, governance, traceability, warehouse rules |
| `.dbt-specify/agents/` | bounded handoff contracts for sub-agents |

Skills are reusable knowledge. Sub-agent templates are role contracts.

## 3. Delegate discovery in parallel

Discovery and review can run in parallel because they should not edit production dbt files.

Example handoffs:

```text
Ask spec-steward to draft the spec for this business request. It may edit only specs/001-*/.
Ask dbt-architect to review lineage and contract impact. It must not edit SQL.
Ask warehouse-optimizer to review materialization and cost decisions. It must not edit SQL.
Ask governance-reviewer to check PII, masking, access, and ownership. It must not edit SQL.
```

Each role should return findings and approval or block status.

## 4. Serialize implementation

Only one implementation agent should edit dbt files at a time:

```text
Use implementation-agent to complete only T1 from tasks.md. Edit only files listed in plan.md for
T1. Stop after validation evidence is recorded.
```

Do not run two implementation agents against the same model or YAML file.

## 5. Review final evidence

Before merge:

```bash
dbt-specify validate project
dbt parse
dbt-specify validate dbt --manifest target/manifest.json
dbt-specify report --format markdown
```

Then hand off to the review role:

```text
Use review-agent to compare the final diff to spec.md, plan.md, tasks.md, and dbt-specify report.
Return findings ordered by severity and recommend approve, request changes, or block.
```

## Success criteria

- Skills are used as knowledge, not as task owners.
- Sub-agents have explicit allowed edit paths.
- Discovery and review can happen in parallel.
- Implementation happens one task at a time.
- Human approval remains the merge gate.
