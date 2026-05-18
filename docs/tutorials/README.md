# Tutorials

These tutorials teach dbt-spec-kit as an operating model, not just a CLI install.

Use them in order when onboarding a team:

| Tutorial | Time | Audience | Outcome |
|---|---:|---|---|
| [1. Initialize a dbt repo](01-initialize-a-dbt-repo.md) | 10 min | Any dbt developer | Add the AI SDLC layer to an existing dbt project |
| [2. Ship a jaffle-shop change](02-jaffle-shop-change.md) | 25 min | Analytics engineers and reviewers | Walk a real dbt feature from business request to review evidence |
| [3. Adopt in a brownfield enterprise repo](03-brownfield-enterprise-adoption.md) | 30 min | Data platform leads | Roll out the workflow without rewriting production models |
| [4. Run skills and sub-agent handoffs](04-skills-and-sub-agent-handoffs.md) | 20 min | Teams using AI agents | Decide when to use skills, sub-agents, and human approval gates |
| [5. Jira to spec workflow](05-jira-to-spec-workflow.md) | 20 min | Enterprise teams using Jira | Pull Jira context into specs and publish approved artifacts back |

## Learning path

```text
Install
  -> initialize .dbt-specify/
  -> write the first spec
  -> approve a plan
  -> implement one task
  -> attach CI evidence
  -> sync approved artifacts to Jira
  -> review and merge
```

The tutorials assume your AI tool can read markdown files in the repo. Claude Code, Codex, Cursor,
GitHub Copilot, Gemini CLI, Cline, and similar tools can all use the generated prompts and context.

## What teams should learn

- Business requests become `spec.md`, not ad hoc SQL changes.
- Plans define file ownership before implementation begins.
- Tasks keep AI agents from editing too much at once.
- dbt Labs skills answer dbt framework questions.
- dbt-spec-kit skills and sub-agent roles enforce enterprise delivery rules.
- CI evidence proves the final diff followed the approved plan.
- Jira remains the intake and task tracking system, while specs remain the engineering contract.
