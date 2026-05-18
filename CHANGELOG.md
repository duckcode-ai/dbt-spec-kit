# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] — 2026-05-18

### Added
- Confluence bridge commands for pulling wiki pages into local spec context, publishing spec
  summaries, and syncing existing Confluence pages from approved artifacts.
- Confluence integration docs and tutorial for knowledge-base context workflows.

## [1.3.0] — 2026-05-18

### Added
- Jira bridge commands for pulling Jira issues into local specs, attaching approved artifacts, and
  creating Jira subtasks from `tasks.md`.
- Jira integration docs and tutorial for enterprise intake workflows.

### Changed
- Clarified README and tutorial command examples so one-off `uvx` usage is not mixed with direct
  `dbt-specify` commands unless the CLI is persistently installed.

## [1.2.0] — 2026-05-18

### Added
- Warehouse presets and guides for Redshift, Postgres, SQL Server, Azure SQL, MySQL, DuckDB,
  MotherDuck, and Athena.
- `/dbt.implement-all` command template for sequential multi-task implementation with validation
  checkpoints and stop conditions.
- Enterprise spec retention and repo hygiene guidance for balancing decision records with repo noise.
- README enterprise adoption choices that surface workflow, retention, rollout, agent, warehouse, and
  CI guidance before the detailed docs list.
- README spec folder structure guidance for large-team feature directories.

## [1.1.0] — 2026-05-18

### Added
- Sub-agent role templates installed to `.dbt-specify/agents/`.
- Enterprise skills for AC traceability, PII/access governance, project convention capture, and CI evidence review.
- Skills and sub-agents documentation showing how dbt-spec-kit composes with dbt-labs/dbt-agent-skills.
- Tutorial series covering initialization, jaffle-shop, brownfield enterprise adoption, and
  skills/sub-agent handoffs.
- README explanation of skills versus sub-agents.
- Launch-ready OSS project files: issue templates, pull request template, SECURITY, SUPPORT, and ROADMAP.
- Jaffle-shop AI SDLC walkthrough using the upstream dbt Labs project as the onboarding demo.
- Team onboarding playbook for introducing dbt-spec-kit to analytics engineering teams.
- Documentation tests for README links, walkthrough commands, and OSS file presence.
- PyPI Trusted Publishing release workflow and maintainer release runbook.

### Changed
- Reworked README around the jaffle-shop quickstart, team adoption path, and CI trust boundary.
- Connected getting-started, brownfield onboarding, enterprise CI, and contributing docs to the new OSS onboarding flow.

## [1.0.0] — 2026-05-18

### Added
- Enterprise validation commands: `dbt-specify validate project`, `dbt-specify validate dbt`,
  `dbt-specify doctor`, `dbt-specify report`, and `dbt-specify ci`.
- CI-ready markdown and JSON validation reports.
- Manifest-aware dbt checks for model descriptions, model tests, mart grain, source freshness,
  and exposures.
- Lifecycle traceability checks across `spec.md`, `plan.md`, and `tasks.md`.
- BigQuery warehouse preset with partitioning, clustering, cost, policy-tag, and BI Engine
  planning guidance.
- Two additional agent commands: `/dbt.analyze` and `/dbt.review`.
- Enterprise CI, brownfield onboarding, and v1 release documentation.

## [0.1.0] — 2026-05-17

### Added
- Initial release.
- `dbt-specify` CLI with `init`, `validate`, `version` commands.
- Base warehouse-agnostic constitution.
- Spec, plan, tasks, and retro templates.
- Snowflake warehouse preset (constitution additions, plan additions, clustering-decisions skill).
- Databricks warehouse preset (constitution additions, plan additions, liquid-clustering-decisions skill).
- Trino warehouse preset (constitution additions, plan additions, federated-query-patterns skill).
- Three skills: writing-staging-model-specs (tier 2), writing-mart-specs-with-grain (tier 2), writing-business-glossary-specs (tier 3).
- Four slash-command prompts: `/dbt.specify`, `/dbt.plan`, `/dbt.tasks`, `/dbt.implement`.
- Worked example: jaffle-shop-staging-overhaul.
- EARS pattern validator for spec Acceptance Criteria.
- CI workflow (lint, type-check, test) on Python 3.11 and 3.12.
