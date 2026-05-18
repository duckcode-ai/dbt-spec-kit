# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Launch-ready OSS project files: issue templates, pull request template, SECURITY, SUPPORT, and ROADMAP.
- Jaffle-shop AI SDLC walkthrough using the upstream dbt Labs project as the onboarding demo.
- Team onboarding playbook for introducing dbt-spec-kit to analytics engineering teams.
- Documentation tests for README links, walkthrough commands, and OSS file presence.

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
