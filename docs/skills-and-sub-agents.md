# Skills and sub-agents

dbt-spec-kit composes with
[dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills) instead of copying it.
dbt Labs owns framework-level dbt mechanics. dbt-spec-kit owns the enterprise AI SDLC layer around
business intent, approved plans, task boundaries, governance, warehouse guardrails, and CI evidence.

## The stack

| Layer | Owner | Purpose |
|---|---|---|
| dbt framework skills | dbt Labs | How dbt works: commands, tests, docs, semantic layer, Mesh, MCP, migration, troubleshooting |
| Project context | Each dbt team | Naming, layering, CTE, ownership, package, and review conventions in `CLAUDE.md` or future `AGENTS.md` |
| Enterprise skills | dbt-spec-kit | Business meaning, grain, warehouse decisions, governance, traceability, and CI evidence |
| Sub-agent roles | dbt-spec-kit | Handoff protocols for bounded workers with file ownership and output contracts |

dbt Labs describes its skills as automatically loaded by agents when the prompt matches a use case,
not slash commands. dbt-spec-kit uses slash-command prompts for the SDLC phases and markdown role
templates for delegation.

## Install dbt Labs skills separately

For Claude Code, install the dbt Labs marketplace and dbt plugin:

```text
/plugin marketplace add dbt-labs/dbt-agent-skills
/plugin install dbt@dbt-agent-marketplace
/plugin install dbt-migration@dbt-agent-marketplace
```

The `/plugin` commands install the skills. They do not change how skills are invoked during dbt
work: after installation, agents load matching skills from natural-language prompts.

Use the Vercel Skills CLI:

```bash
npx skills add dbt-labs/dbt-agent-skills
npx skills add dbt-labs/dbt-agent-skills --skill using-dbt-for-analytics-engineering
```

Or use Tessl:

```bash
tessl install dbt-labs/dbt-agent-skills
tessl install dbt-labs/dbt-agent-skills --skill using-dbt-for-analytics-engineering
```

Do not vendor dbt Labs skills into your dbt repo unless your organization has a specific mirroring
policy. Prefer installing them through the supported skill tooling and referencing them from
`CLAUDE.md`.

## Skill routing

| dbt Labs skill family | Use during dbt-spec-kit phase | dbt-spec-kit complement |
|---|---|---|
| `using-dbt-for-analytics-engineering` | Plan, implement, review | Enforce approved spec, file list, and project conventions |
| `adding-dbt-unit-test` | Plan, tasks, implement | Map tests to AC ids and CI evidence |
| `building-dbt-semantic-layer` | Specify, plan, review | Capture metric compatibility and downstream impact |
| `working-with-dbt-mesh` | Plan, review | Capture ownership, contracts, exposures, and cross-team impact |
| `running-dbt-commands` | Implement, review, CI | Require validation commands in tasks and reports |
| `fetching-dbt-docs` | Specify, plan, review | Keep dbt framework facts current without weakening local rules |
| Troubleshooting and migration skills | Implement, review | Record findings without silently expanding scope |

## Skills versus sub-agents

Skills are reusable knowledge. A skill tells the current agent how to do a category of work better:
write a mart spec with grain, choose a Snowflake clustering key, review PII handling, or check AC
traceability.

Sub-agents are bounded workers. A sub-agent role says what context to read, which files it may edit,
which files it must not touch, and what output it must return.

Example:

```text
Business request
  -> spec-steward uses spec-writing and business glossary skills
  -> dbt-architect uses dbt Labs skills for framework mechanics
  -> warehouse-optimizer uses warehouse-specific dbt-spec-kit skills
  -> implementation-agent edits one approved task
  -> governance-reviewer checks PII and access
  -> review-agent checks AC coverage and CI evidence
```

## Installed role templates

`dbt-specify init` installs these templates into `.dbt-specify/agents/`:

| Role | Responsibility |
|---|---|
| `spec-steward` | Convert a business request into a reviewed `spec.md` |
| `dbt-architect` | Review model design, lineage, contracts, and dbt Labs skill usage |
| `warehouse-optimizer` | Review warehouse cost, materialization, partitioning, and clustering decisions |
| `implementation-agent` | Implement exactly one approved task and stop |
| `governance-reviewer` | Review PII, access, contracts, ownership, and policy-sensitive changes |
| `review-agent` | Check final diff against ACs, plan, tests, and `dbt-specify report` |

## Delegation rules

- Parallelize discovery and review only.
- Serialize implementation by task.
- Never let two agents edit the same dbt model or YAML file concurrently.
- Keep implementation inside the approved plan's file list.
- Human approval remains the merge gate.

For a hands-on sequence, follow
[Tutorial 4: Run skills and sub-agent handoffs](tutorials/04-skills-and-sub-agent-handoffs.md).
