# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
