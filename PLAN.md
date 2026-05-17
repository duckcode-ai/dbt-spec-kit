# dbt-spec-kit — v0.1 Build Plan

**Hand-off document for Claude Code.** Read this end-to-end before touching code. Every section is here on purpose. If something is ambiguous, prefer the choice this document recommends over your own intuition; this plan was specifically designed to eliminate the questions you would otherwise ask.

---

## How to use this document

You are an autonomous coding agent. You are being handed a fully-specified open-source project to build from scratch. The human has already done the research, validated the wedge, and made the scope decisions. Your job is to ship v0.1.

**Read order:**
1. Section 1 (Mission) — *why* this project exists, in one page
2. Section 2 (Constitution) — *non-negotiable* principles you must never violate
3. Section 3 (Spec) — *what* v0.1 is, with acceptance criteria
4. Section 4 (Plan) — *how* — file-by-file build plan
5. Section 5 (Tasks) — *ordered* work breakdown with checkboxes
6. Sections 6–9 — reference appendices for templates, content, edge cases

**Working agreement:**
- Implement in the order of Section 5
- After each numbered task, run the validation step in that task and only proceed once green
- Do not add features not in this plan — if you spot a gap, surface it as a `FOLLOWUP.md` entry, do not build it
- Use the `git commit` convention from Section 2 §6 (one commit per task, message includes task id)
- All code paths and prose follow the style rules in Section 2 §7
- If a section conflicts with another, the Constitution (Section 2) wins
- If you have a question that this document doesn't answer, write it to `QUESTIONS.md` and pick the answer that best aligns with the Mission (Section 1) and Constitution (Section 2)

---

## 1. Mission

### 1.1 What this is

`dbt-spec-kit` is an open-source toolkit that brings **Spec-Driven Development (SDD)** to **dbt-centric data engineering**, with **warehouse-specific presets** for Snowflake, Databricks, and Trino.

It is modeled directly on [github/spec-kit](https://github.com/github/spec-kit) (the reference SDD implementation) and [IBM/iac-spec-kit](https://github.com/IBM/iac-spec-kit) (the precedent for vertical adaptation). It composes with [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills) — it does not replace or compete with it.

### 1.2 The four-phase loop, dbt-flavored

| Phase | What happens | Artifact produced |
|---|---|---|
| **Specify** | Engineer writes what data product is needed, who uses it, success criteria | `specs/<NNN>-<slug>/spec.md` |
| **Plan** | Agent proposes file-by-file plan (models, sources, tests, exposures); engineer approves | `specs/<NNN>-<slug>/plan.md` |
| **Tasks** | Plan decomposes into ordered, testable units of work | `specs/<NNN>-<slug>/tasks.md` |
| **Implement** | Agent writes models, tests, docs; runs `dbt build`; iterates | dbt project changes |

Every phase has a **human checkpoint**. No auto-merge. No skipping plan review.

### 1.3 The three positioning pillars (this is the whole project in one table)

| Pillar | What we ship | Why it's defensible |
|---|---|---|
| **Methodology layer** | Constitution, spec/plan/tasks templates, four-phase CLI | dbt Labs ships skills (how-to) and agents (runtime); nobody has shipped a spec-kit-style methodology layer specifically for dbt |
| **Warehouse presets** | Snowflake-, Databricks-, and Trino-flavored constitutions + plan additions | dbt Labs is intentionally warehouse-agnostic and will not go here; this is the deepest moat |
| **Tier-3 (business domain) skills** | Skills for writing business glossaries, grain definitions, entity-resolution specs | Community skills cover dbt mechanics; project CLAUDE.md files cover team conventions; tier 3 — what your business actually is — is unaddressed by anyone |

### 1.4 What we explicitly are NOT

- We are **not** a replacement for `dbt-labs/dbt-agent-skills` — we compose with it. Users install both.
- We are **not** an alternative to `dbt deps` packages — those are runtime code; we ship process artifacts.
- We are **not** an IDE — we ship markdown templates and a thin CLI, not a UI.
- We are **not** opinionated about which AI agent is used — we work with any agent that reads markdown context (Claude Code, Cursor, Copilot, Gemini CLI, Cline, etc.).

### 1.5 Who this is for

- **Primary**: dbt practitioners (analytics engineers, data engineers, data platform engineers) using AI coding agents on dbt projects.
- **Secondary**: data engineering leads who want to standardize how their team uses AI on dbt work.
- **Tertiary**: dbt consultancies who want a reusable methodology to bring to clients.

### 1.6 Success criteria for v0.1

The project is "done" when:
1. A user runs `uvx --from git+https://github.com/duckcode-ai/dbt-spec-kit.git dbt-specify init my-project --warehouse <snowflake|databricks|trino>` and gets a working `.dbt-specify/` directory in their existing dbt project.
2. The user can invoke `/dbt.specify`, `/dbt.plan`, `/dbt.tasks`, `/dbt.implement` slash commands in Claude Code (and the prompts cleanly map to other agents that load markdown context).
3. The user can run `dbt-specify validate specs/001-my-feature/spec.md` and get useful EARS-style feedback.
4. The README is good enough that a stranger can decide in <60 seconds whether to use it.
5. The `examples/jaffle-shop-staging-overhaul/` worked example traces a real-looking dbt ticket through all four artifacts (spec → plan → tasks → implementation summary) end-to-end.
6. CI is green on a fresh clone (lint, unit tests, schema validation).
7. The repo is `uvx`-installable and the install path is documented.

---

## 2. Constitution

These are the non-negotiable principles for the project itself. They are enforced during every phase. If any later section conflicts with this one, this section wins.

### §1. Composition over replacement
We compose with `dbt-labs/dbt-agent-skills`, `dbt-core`, and `dbt-fusion`. We do not duplicate skills that already exist there. If a user asks "how do I add a unit test?" the answer is to install `dbt-agent-skills`, not to reinvent that content here.

### §2. Markdown is the only required artifact format
All templates, constitutions, specs, plans, and tasks are markdown. Not JSON, not YAML schemas, not custom DSLs. The format must be readable by any human and any current-generation LLM agent without preprocessing.

### §3. Warehouse-specific differentiation is the moat
The base constitution is warehouse-agnostic. Each warehouse preset adds — never overrides — warehouse-specific principles (clustering keys, masking policies, Liquid Clustering, Photon, Unity Catalog, etc.). A user who picks `--warehouse snowflake` gets the base constitution PLUS Snowflake-specific additions. The presets are where we win.

### §4. Tier-3 skills are first-class
Most agent skills today are tier 1 (framework conventions) or tier 2 (team/project conventions). We ship at least one tier-3 skill in v0.1: writing business glossary specs. This is the part nobody else does.

### §5. EARS notation is the spec testing format
Every acceptance criterion in a spec MUST be expressible as an EARS statement (Easy Approach to Requirements Syntax):
- Ubiquitous: "The system shall <response>."
- Event-driven: "When <trigger>, the system shall <response>."
- State-driven: "While <state>, the system shall <response>."
- Unwanted: "If <unwanted condition>, then the system shall <response>."
- Optional: "Where <feature is included>, the system shall <response>."

A `validate` command checks ACs against EARS patterns and warns on non-conformant phrasing.

### §6. Git commits are atomic and traceable
Each task in Section 5 maps to one commit. Commit message format: `<task-id>: <imperative summary>` (e.g., `T-04: add base constitution.md`). No commits without a task id during the v0.1 build.

### §7. Style — code and prose

**Code (Python CLI):**
- Python 3.11+
- Type hints on every function signature
- `ruff` for lint, `mypy` for type-checking (both must pass in CI)
- No global state. All state passes through function arguments or class instances.
- Prefer `pathlib.Path` over `os.path`
- Stdlib first; only add a dependency if it materially saves work (Click for CLI, Jinja2 for template rendering — both already in spec-kit's transitive dependencies if reused)

**Markdown (templates and docs):**
- Sentence-case headers (`## What this template is for`, not `## What This Template Is For`)
- No emoji in template content (emoji is fine in marketing copy in README; never in things users will fill in or that agents will parse)
- Line length: soft 100 chars for prose, hard 120 for code blocks; never enforced by trailing-whitespace linters that munge text
- Every template starts with a `<!-- INSTRUCTIONS: ... -->` block telling the agent (or user) how to fill it in. Remove instructions on save? No — they stay; they're cheap and useful for the next iteration.

### §8. No telemetry
The CLI does not phone home. No usage tracking, no analytics endpoints, no version-check pings without an explicit `--check-update` flag. This is open source for actual humans, not a funnel.

### §9. License
MIT. Mirrors `github/spec-kit` and `dbt-labs/dbt-agent-skills`.

### §10. No screenshots in the repo (yet)
Screenshots become stale fast and bloat the repo. v0.1 ships text-only. README links to demos (asciinema, terminalizer outputs) hosted elsewhere if needed.

---

## 3. Spec (what v0.1 is)

### 3.1 Problem statement

dbt practitioners using AI coding agents — especially on greenfield projects, multi-warehouse projects, or projects that span multiple data domains — face three failure modes:

1. **Intent drift.** "Build a customer mart" produces wildly different things depending on agent context. The agent doesn't know what grain, what SCD strategy, what governance, what warehouse-specific patterns to follow.
2. **Convention decay.** As projects grow, the agent's working memory of project conventions decays. CLAUDE.md helps but is unstructured.
3. **Unverifiable output.** Without explicit acceptance criteria written in a testable form (EARS), there's no way to validate whether a generated dbt model is "right." Code review becomes endless.

`dbt-spec-kit` addresses all three by making specs the source of truth — versioned, structured, warehouse-aware, and agent-readable.

### 3.2 Users and the jobs they hire this for

| User | Job |
|---|---|
| Analytics engineer at mid-size company | "I want my AI agent to stop generating staging models that don't match our team's CTE pattern." |
| Data platform engineer at enterprise | "I want my five contractors to use the same spec → plan → ship loop, with warehouse-specific guardrails baked in." |
| dbt consultancy | "I want a reusable methodology I can bring to every new client engagement, instead of reinventing CLAUDE.md every project." |
| Open-source contributor | "I want a stable template my community-contributed skills can build on." |

### 3.3 Acceptance criteria (EARS-formatted)

**AC1 (Ubiquitous)** — The system shall ship a `dbt-specify` Python CLI installable via `uvx --from git+...`.

**AC2 (Event-driven)** — When `dbt-specify init <name> --warehouse snowflake` is invoked in a directory containing a `dbt_project.yml`, the system shall create a `.dbt-specify/` directory at the project root containing `constitution.md`, `templates/`, and `presets/snowflake/` content.

**AC3 (Event-driven)** — When `dbt-specify init <name> --warehouse databricks` is invoked, the system shall produce a `.dbt-specify/` directory configured with the Databricks preset.

**AC3a (Event-driven)** — When `dbt-specify init <name> --warehouse trino` is invoked, the system shall produce a `.dbt-specify/` directory configured with the Trino preset.

**AC4 (Unwanted)** — If `dbt-specify init` is run in a directory without a `dbt_project.yml`, the system shall exit with a non-zero status and an error message that names the missing file and points to the docs.

**AC5 (Ubiquitous)** — The system shall provide four slash-command prompt files that map to Claude Code's slash command format: `/dbt.specify`, `/dbt.plan`, `/dbt.tasks`, `/dbt.implement`.

**AC6 (Event-driven)** — When `dbt-specify validate <path-to-spec>` is invoked, the system shall parse the spec's Acceptance Criteria section and report any line that doesn't match an EARS pattern.

**AC7 (Ubiquitous)** — The system shall ship an `examples/jaffle-shop-staging-overhaul/` directory containing a complete spec → plan → tasks → implementation summary chain demonstrating the full loop.

**AC8 (Ubiquitous)** — The system shall ship at least one tier-3 (business domain) skill: `writing-business-glossary-specs/SKILL.md`.

**AC9 (Ubiquitous)** — The system shall include a CI workflow (GitHub Actions) that runs on every PR with three required checks: lint (ruff), type-check (mypy), and unit tests (pytest).

**AC10 (Optional)** — Where the user has `dbt-labs/dbt-agent-skills` installed, the system shall produce CLAUDE.md output that explicitly defers tier-1 questions to that skill collection rather than duplicating it.

### 3.4 Out of scope for v0.1

The following are explicitly **not** in v0.1. Do not build them. If you spot a strong case for building one, write a `FOLLOWUP.md` entry — do not implement.

- BigQuery preset (v0.2)
- Redshift preset (v0.3)
- An emerging Iceberg-engine preset (Tabular / DuckDB-Wasm / others) (v0.4+)
- A web UI or VS Code extension
- A registry/hub for community-contributed presets
- Auto-generation of skills from existing dbt projects
- Integration with `dbt deps` `skills:` key (block on `dbt-core` issue #12868 shipping)
- Interactive prompts beyond the minimum needed for `init` (the CLI is mostly non-interactive — pass flags, get output)
- Sub-commands beyond `init`, `validate`, `version` (e.g., no `add-preset`, no `update`, no `lint` — v0.2+)
- Multi-tenant or org-level configuration
- Anything involving an LLM API call from the CLI (the CLI is offline; the LLM lives in the user's chosen agent)
- Telemetry, metrics, or auto-update mechanisms

### 3.5 Constraints

- Python 3.11+ only. No backward compatibility with 3.10.
- Linux, macOS, Windows must all work. Test on macOS (assumed dev env); CI runs Ubuntu.
- Project must be installable in <30 seconds on a typical broadband connection.
- Generated `.dbt-specify/` directory should be <500 KB total.
- Zero runtime dependencies outside Python stdlib + Click + Jinja2 + a single YAML library (PyYAML).
- The CLI must work without network access after install (no runtime template fetching).

---

## 4. Plan (how — file by file)

### 4.1 Repository layout

The repository you will create looks like this. Treat this as the authoritative file list. If a path is not in this tree, do not create it without a `FOLLOWUP.md` entry.

```
dbt-spec-kit/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── pyproject.toml
├── PLAN.md                              # this file (keep it in the repo; users will read it)
├── FOLLOWUP.md                          # ideas you noticed but didn't build
├── QUESTIONS.md                         # questions you couldn't answer from this plan
│
├── src/
│   └── dbt_specify/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── init.py
│       ├── validate.py
│       ├── ears.py
│       ├── templates_loader.py
│       └── _version.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_init.py
│   ├── test_validate.py
│   ├── test_ears.py
│   └── fixtures/
│       ├── valid_spec.md
│       ├── invalid_spec_non_ears.md
│       └── minimal_dbt_project/
│           ├── dbt_project.yml
│           └── models/
│               └── .gitkeep
│
├── memory/
│   └── constitution.md                  # the base, warehouse-agnostic dbt SDD constitution
│
├── templates/
│   ├── spec-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   ├── retro-template.md
│   └── CLAUDE.md.template
│
├── presets/
│   ├── snowflake/
│   │   ├── constitution-additions.md
│   │   ├── plan-additions.md
│   │   └── skills/
│   │       └── snowflake-clustering-decisions/
│   │           └── SKILL.md
│   ├── databricks/
│   │   ├── constitution-additions.md
│   │   ├── plan-additions.md
│   │   └── skills/
│   │       └── databricks-liquid-clustering-decisions/
│   │           └── SKILL.md
│   └── trino/
│       ├── constitution-additions.md
│       ├── plan-additions.md
│       └── skills/
│           └── trino-federated-query-patterns/
│               └── SKILL.md
│
├── skills/
│   ├── writing-staging-model-specs/
│   │   └── SKILL.md
│   ├── writing-mart-specs-with-grain/
│   │   └── SKILL.md
│   └── writing-business-glossary-specs/
│       └── SKILL.md
│
├── commands/                            # slash-command prompts for AI agents
│   ├── dbt.specify.md
│   ├── dbt.plan.md
│   ├── dbt.tasks.md
│   └── dbt.implement.md
│
├── examples/
│   └── jaffle-shop-staging-overhaul/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── implementation-summary.md
│
└── docs/
    ├── getting-started.md
    ├── methodology.md
    ├── ears-cheatsheet.md
    └── warehouse-guides/
        ├── snowflake.md
        ├── databricks.md
        └── trino.md
```

Total: ~50 files. Most are markdown content — only ~7 Python files.

### 4.2 What goes in each file (one-line purpose for each)

**Top-level:**

| Path | Purpose |
|---|---|
| `LICENSE` | MIT. Copy from spec-kit verbatim, update copyright holder. |
| `README.md` | The 60-second pitch. Section 7 of this plan has the full content. |
| `CHANGELOG.md` | Start with `## 0.1.0 — <today's date>` and an unreleased section. |
| `CONTRIBUTING.md` | How to add a warehouse preset, how to write a SKILL.md, how to run tests locally. |
| `pyproject.toml` | Project metadata, dependencies, console_scripts entry point. Section 6.1 has the full content. |
| `PLAN.md` | This file — keep it. |
| `FOLLOWUP.md` | Start empty with a header explaining what it's for. |
| `QUESTIONS.md` | Start empty with a header. Only used if you hit ambiguity. |

**`src/dbt_specify/`** (the Python CLI — small, deliberately):

| Path | Purpose |
|---|---|
| `__init__.py` | Empty, or just `__version__` import. |
| `__main__.py` | One-liner: `from .cli import main; main()` for `python -m dbt_specify`. |
| `cli.py` | Click command group with `init`, `validate`, `version` subcommands. Section 6.2 has full code. |
| `init.py` | The `init` command implementation. Copies templates and presets into target dir. Section 6.3. |
| `validate.py` | The `validate` command. Parses a spec.md, checks AC section for EARS conformance. Section 6.4. |
| `ears.py` | EARS pattern matchers. Pure functions. Section 6.5 has full code. |
| `templates_loader.py` | Reads from the installed package data (templates/, presets/, etc.). Section 6.6. |
| `_version.py` | Single line: `__version__ = "0.1.0"`. |

**`tests/`** — pytest tests for the CLI. Section 6.7 has full structure.

**`memory/constitution.md`** — the base constitution, warehouse-agnostic. Section 8.1 has full content.

**`templates/`** — the four-phase artifact templates:

| Template | Purpose |
|---|---|
| `spec-template.md` | Template the user (or agent) fills in during the Specify phase. Section 8.2. |
| `plan-template.md` | Template for the Plan phase. Section 8.3. |
| `tasks-template.md` | Template for the Tasks phase. Section 8.4. |
| `retro-template.md` | Template for the post-ship retro. Section 8.5. |
| `CLAUDE.md.template` | What `init` writes as the project's CLAUDE.md if one doesn't exist (and offers to merge if one does). Section 8.6. |

**`presets/snowflake/`**:

| Path | Purpose |
|---|---|
| `constitution-additions.md` | Snowflake-specific principles APPENDED to the base constitution. Section 8.7. |
| `plan-additions.md` | Snowflake-specific sections appended to the plan template (clustering, warehouse sizing, masking, query tags). Section 8.8. |
| `skills/snowflake-clustering-decisions/SKILL.md` | When to use clustering keys on Snowflake, with concrete heuristics. Section 8.9. |

**`presets/databricks/`** — same structure, Databricks-flavored. Section 8.10–8.12.

**`presets/trino/`** — same structure, Trino-flavored. Section 8.12a–8.12c.

**`skills/`** — three tier-2/tier-3 SKILL.md files:

| Path | Tier | Purpose |
|---|---|---|
| `writing-staging-model-specs/SKILL.md` | Tier 2 | How to write a spec for a dbt staging model. Section 8.13. |
| `writing-mart-specs-with-grain/SKILL.md` | Tier 2 | How to write a mart spec that's explicit about grain. Section 8.14. |
| `writing-business-glossary-specs/SKILL.md` | **Tier 3** | The wedge skill: writing entity-resolution and business-glossary specs. Section 8.15. |

**`commands/`** — slash-command prompts. Each is a markdown file containing the agent instruction for one phase. Section 8.16–8.19.

**`examples/jaffle-shop-staging-overhaul/`** — a worked example:

| Path | Purpose |
|---|---|
| `spec.md` | A realistic spec for "rewrite the jaffle-shop staging layer to follow our new conventions." Section 8.20. |
| `plan.md` | The plan the agent produced and the engineer approved. Section 8.21. |
| `tasks.md` | The task breakdown. Section 8.22. |
| `implementation-summary.md` | A retro-flavored summary of what was built, what changed in CLAUDE.md after ship. Section 8.23. |

**`docs/`** — supporting documentation:

| Path | Purpose |
|---|---|
| `getting-started.md` | 5-minute install + first spec + first plan. Section 9.1. |
| `methodology.md` | The full four-phase loop explained in depth. Section 9.2. |
| `ears-cheatsheet.md` | EARS patterns with dbt-flavored examples. Section 9.3. |
| `warehouse-guides/snowflake.md` | Detailed guide for Snowflake users. Section 9.4. |
| `warehouse-guides/databricks.md` | Detailed guide for Databricks users. Section 9.5. |
| `warehouse-guides/trino.md` | Detailed guide for Trino users. Section 9.6. |

**`.github/workflows/ci.yml`** — three checks: lint, mypy, pytest. Section 6.8.

### 4.3 Risk surface (where things can go wrong)

| Risk | Likelihood | Mitigation |
|---|---|---|
| Template rendering breaks on Windows path separators | Medium | Always use `pathlib.Path`; tests run on Ubuntu but path logic is platform-agnostic. |
| EARS validator has false positives (rejects valid specs) | Medium | Ship the regex patterns in Section 6.5 verbatim; if a user reports a false positive, add a fixture and patch — do NOT loosen the patterns. |
| User's existing `CLAUDE.md` gets clobbered by `init` | High if not careful | NEVER overwrite an existing `CLAUDE.md`. If one exists, write `CLAUDE.md.dbt-specify-suggested` next to it and print a message explaining how to merge. |
| User's existing `.dbt-specify/` from a prior `init` gets clobbered | High | `init` refuses to overwrite by default. Require `--force` flag. |
| dbt Labs ships something that overlaps (dbt Agents goes GA) | High over 3-6 months | Out of v0.1 scope; positioning in README is explicit about composition with their work. |
| Warehouse preset additions conflict with base constitution | Low | Presets are strictly ADDITIVE — they don't repeal base principles, they only add warehouse-specific ones. Linter check: a preset constitution should never contain a `~~strikethrough~~` of a base principle. |
| Tier-3 skill (business glossary) feels like consulting boilerplate | Medium | Anchor it to the dbt-core discussion #12521's "Well/Unit/Property" entity-resolution example — that's the actual customer voice. |
| Trino is NOT a warehouse — applying "warehouse" framing produces awkward content | Medium | Trino preset frames itself as a "query engine + connector" preset; constitution Article T-* explicitly calls out that storage decisions live in the underlying connector (Iceberg / Delta / Hive), not in Trino itself. |
| Three warehouse presets means three places to keep current | Low for v0.1; higher over time | Article 13 already commits to composition with dbt-labs; for warehouse-specific releases, follow the dbt-trino / dbt-databricks / dbt-snowflake adapters' minor versions and rev presets when ecosystem patterns shift. |

---

## 5. Tasks (ordered, with checkboxes)

Each task has: a unique id, a clear definition of done, and an acceptance test. Implement in order. Commit after each task using the message format `T-NN: <imperative summary>`.

### Phase A — Foundation (Tasks T-01 to T-08)

- [ ] **T-01** — Initialize the repo with `pyproject.toml`, `LICENSE`, `.gitignore`, empty `src/dbt_specify/`, empty `tests/`, empty `memory/`, empty `templates/`, empty `presets/`, empty `skills/`, empty `commands/`, empty `examples/`, empty `docs/`. Use the directory tree from Section 4.1.
  - **Done when**: `git status` shows the tree exactly matches Section 4.1 (empty files are fine for now, use `.gitkeep` where the dir would otherwise be empty).
  - **Acceptance**: Run `tree -L 3 .` and confirm against Section 4.1.

- [ ] **T-02** — Write `pyproject.toml` using the content from Section 6.1.
  - **Done when**: `pip install -e .` succeeds in a fresh venv and `dbt-specify --version` runs.
  - **Acceptance**: `pip install -e . && dbt-specify --version` prints `0.1.0`.

- [ ] **T-03** — Write `src/dbt_specify/_version.py` (one line) and `src/dbt_specify/cli.py` (Click skeleton from Section 6.2).
  - **Done when**: `dbt-specify --help` shows `init`, `validate`, `version` subcommands.
  - **Acceptance**: `dbt-specify --help` exits 0 and shows all three subcommands.

- [ ] **T-04** — Write `memory/constitution.md` using the content from Section 8.1.
  - **Done when**: The file exists and is ~120 lines. Headers are sentence-case.
  - **Acceptance**: `wc -l memory/constitution.md` returns 100–150.

- [ ] **T-05** — Write the four template files in `templates/` (spec, plan, tasks, retro) from Sections 8.2–8.5.
  - **Done when**: Each file starts with an `<!-- INSTRUCTIONS: ... -->` block and is ready for a user to fill in.
  - **Acceptance**: `ls templates/ | wc -l` returns 5 (the four phase templates + CLAUDE.md.template).

- [ ] **T-06** — Write `templates/CLAUDE.md.template` using the content from Section 8.6.
  - **Done when**: The template references the base constitution at `.dbt-specify/constitution.md` and defers tier-1 questions to dbt-agent-skills.

- [ ] **T-07** — Write `src/dbt_specify/templates_loader.py` using Section 6.6.
  - **Done when**: A Python REPL can `from dbt_specify.templates_loader import load_template; print(load_template('spec'))` and get the template content.
  - **Acceptance**: Add a quick smoke test in `tests/test_init.py` that imports and calls `load_template`.

- [ ] **T-08** — Wire up package data in `pyproject.toml` so templates, presets, skills, and commands directories are included in the installed wheel. Add an integration test that confirms a fresh `pip install -e .` can still load all templates from the installed location.
  - **Done when**: `python -c "from dbt_specify.templates_loader import load_template; print(load_template('spec'))"` runs from any directory.

### Phase B — The `init` command (T-09 to T-14)

- [ ] **T-09** — Implement `src/dbt_specify/init.py` per Section 6.3.
  - **Done when**: The function `init_project(project_name, warehouse, target_dir, force)` exists and is fully typed.

- [ ] **T-10** — Wire `init.py` into the `cli.py` command group.
  - **Done when**: `dbt-specify init --help` shows all flags (`--warehouse`, `--force`, `--target`).

- [ ] **T-11** — Write unit tests for `init` in `tests/test_init.py` (the structure is in Section 6.7).
  - **Done when**: Tests cover: success case, missing `dbt_project.yml` exit, existing `.dbt-specify/` without `--force`, existing `.dbt-specify/` with `--force`, both warehouse presets.
  - **Acceptance**: `pytest tests/test_init.py -v` shows ≥5 tests passing.

- [ ] **T-12** — Add `tests/fixtures/minimal_dbt_project/` per Section 4.1.
  - **Done when**: The fixture contains a minimal valid `dbt_project.yml`.

- [ ] **T-13** — End-to-end smoke test: run `dbt-specify init test-project --warehouse snowflake` against the fixture and verify the produced `.dbt-specify/` directory contains the expected files (constitution, templates, snowflake preset).
  - **Done when**: A test in `test_init.py` performs this end-to-end check.

- [ ] **T-14** — End-to-end smoke test for Databricks preset.
  - **Done when**: Same as T-13 but for `--warehouse databricks`.

- [ ] **T-14a** — End-to-end smoke test for Trino preset.
  - **Done when**: Same as T-13 but for `--warehouse trino`. The test asserts the produced constitution.md contains "Federation" (Trino is a federated query engine — that word should appear in the additions).

### Phase C — Warehouse presets (T-15 to T-23)

- [ ] **T-15** — Write `presets/snowflake/constitution-additions.md` per Section 8.7.

- [ ] **T-16** — Write `presets/snowflake/plan-additions.md` per Section 8.8.

- [ ] **T-17** — Write `presets/snowflake/skills/snowflake-clustering-decisions/SKILL.md` per Section 8.9.

- [ ] **T-18** — Write `presets/databricks/constitution-additions.md` per Section 8.10.

- [ ] **T-19** — Write `presets/databricks/plan-additions.md` per Section 8.11.

- [ ] **T-20** — Write `presets/databricks/skills/databricks-liquid-clustering-decisions/SKILL.md` per Section 8.12.

- [ ] **T-21** — Write `presets/trino/constitution-additions.md` per Section 8.12a. **Note**: Trino is a query engine, not a warehouse — the constitution frames itself differently. Read Section 8.12a's opening note carefully.

- [ ] **T-22** — Write `presets/trino/plan-additions.md` per Section 8.12b.

- [ ] **T-23** — Write `presets/trino/skills/trino-federated-query-patterns/SKILL.md` per Section 8.12c.

### Phase D — Tier-2 and Tier-3 skills (T-24 to T-26)

- [ ] **T-24** — Write `skills/writing-staging-model-specs/SKILL.md` per Section 8.13.

- [ ] **T-25** — Write `skills/writing-mart-specs-with-grain/SKILL.md` per Section 8.14.

- [ ] **T-26** — Write `skills/writing-business-glossary-specs/SKILL.md` per Section 8.15. **This is the wedge skill — spend extra care.**

### Phase E — Slash commands (T-27 to T-30)

- [ ] **T-27** — Write `commands/dbt.specify.md` per Section 8.16.

- [ ] **T-28** — Write `commands/dbt.plan.md` per Section 8.17.

- [ ] **T-29** — Write `commands/dbt.tasks.md` per Section 8.18.

- [ ] **T-30** — Write `commands/dbt.implement.md` per Section 8.19.

### Phase F — The `validate` command (T-31 to T-34)

- [ ] **T-31** — Implement `src/dbt_specify/ears.py` per Section 6.5.
  - **Done when**: Five EARS pattern matchers exist and each has a docstring.

- [ ] **T-32** — Implement `src/dbt_specify/validate.py` per Section 6.4. Wire into CLI.
  - **Done when**: `dbt-specify validate path/to/spec.md` runs and exits 0 if all ACs match an EARS pattern; 1 otherwise.

- [ ] **T-33** — Write `tests/test_ears.py` covering each EARS pattern with positive and negative cases.

- [ ] **T-34** — Write `tests/test_validate.py` using fixtures `valid_spec.md` and `invalid_spec_non_ears.md` (Section 6.7 has both fixtures' content).

### Phase G — Worked example (T-35 to T-38)

- [ ] **T-35** — Write `examples/jaffle-shop-staging-overhaul/spec.md` per Section 8.20.

- [ ] **T-36** — Write `examples/jaffle-shop-staging-overhaul/plan.md` per Section 8.21.

- [ ] **T-37** — Write `examples/jaffle-shop-staging-overhaul/tasks.md` per Section 8.22.

- [ ] **T-38** — Write `examples/jaffle-shop-staging-overhaul/implementation-summary.md` per Section 8.23.

### Phase H — Docs and CI (T-39 to T-46)

- [ ] **T-39** — Write `docs/getting-started.md` per Section 9.1.

- [ ] **T-40** — Write `docs/methodology.md` per Section 9.2.

- [ ] **T-41** — Write `docs/ears-cheatsheet.md` per Section 9.3.

- [ ] **T-42** — Write `docs/warehouse-guides/snowflake.md` per Section 9.4.

- [ ] **T-43** — Write `docs/warehouse-guides/databricks.md` per Section 9.5.

- [ ] **T-44** — Write `docs/warehouse-guides/trino.md` per Section 9.6.

- [ ] **T-45** — Write `.github/workflows/ci.yml` per Section 6.8.
  - **Done when**: A PR triggers lint, mypy, and pytest in CI and all three are green.

- [ ] **T-46** — Write the README, CHANGELOG, CONTRIBUTING files per Section 7.

### Phase I — Final polish (T-47 to T-50)

- [ ] **T-47** — Run the full test suite locally and confirm green. Fix anything that's not.

- [ ] **T-48** — Run `dbt-specify init test-snowflake --warehouse snowflake` against the fixture and visually inspect the output. Repeat for `databricks` and `trino`. All three should produce a clean, professional-looking `.dbt-specify/` directory.

- [ ] **T-49** — Verify the README renders well on GitHub (no broken images, all links work). Confirm the worked example links to the spec/plan/tasks files correctly.

- [ ] **T-50** — Remove `HANDOFF.md` from the repo (it was operational, not user-facing), tag `v0.1.0`, and confirm `uvx --from git+https://github.com/duckcode-ai/dbt-spec-kit.git dbt-specify init test-project --warehouse trino` works end-to-end against the fixture.

---

## 6. Code appendix

Full code/config content for each Python file and the CI workflow. Copy these verbatim unless you spot a bug.

### 6.1 `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "dbt-spec-kit"
version = "0.1.0"
description = "Spec-driven development toolkit for dbt-centric data engineering, with warehouse-specific presets for Snowflake, Databricks, and Trino."
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.11"
authors = [
    { name = "duckcode-ai", email = "open-source@duckcode.ai" }
]
keywords = ["dbt", "spec-driven-development", "ai-agents", "analytics-engineering", "snowflake", "databricks", "trino"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
dependencies = [
    "click>=8.1",
    "jinja2>=3.1",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.4",
    "mypy>=1.10",
    "types-PyYAML",
]

[project.scripts]
dbt-specify = "dbt_specify.cli:main"

[project.urls]
Homepage = "https://github.com/duckcode-ai/dbt-spec-kit"
Repository = "https://github.com/duckcode-ai/dbt-spec-kit"
Issues = "https://github.com/duckcode-ai/dbt-spec-kit/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/dbt_specify"]

[tool.hatch.build.targets.wheel.force-include]
"memory" = "dbt_specify/_assets/memory"
"templates" = "dbt_specify/_assets/templates"
"presets" = "dbt_specify/_assets/presets"
"skills" = "dbt_specify/_assets/skills"
"commands" = "dbt_specify/_assets/commands"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "A", "C4", "RET", "SIM"]
ignore = []

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --cov=dbt_specify --cov-report=term-missing"
```

### 6.2 `src/dbt_specify/cli.py`

```python
"""Click command group for the dbt-specify CLI."""
from __future__ import annotations

from pathlib import Path

import click

from dbt_specify._version import __version__
from dbt_specify.init import init_project
from dbt_specify.validate import validate_spec


@click.group()
@click.version_option(__version__, prog_name="dbt-specify")
def main() -> None:
    """dbt-specify — spec-driven development for dbt projects."""


@main.command()
@click.argument("project_name")
@click.option(
    "--warehouse",
    type=click.Choice(["snowflake", "databricks", "trino"], case_sensitive=False),
    required=True,
    help="Warehouse preset to install alongside the base constitution.",
)
@click.option(
    "--target",
    "target_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("."),
    help="Target directory (default: current directory).",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite an existing .dbt-specify/ directory.",
)
def init(project_name: str, warehouse: str, target_dir: Path, force: bool) -> None:
    """Initialize dbt-specify in an existing dbt project."""
    init_project(
        project_name=project_name,
        warehouse=warehouse.lower(),
        target_dir=target_dir.resolve(),
        force=force,
    )


@main.command()
@click.argument(
    "spec_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def validate(spec_path: Path) -> None:
    """Validate that a spec.md's Acceptance Criteria are EARS-conformant."""
    exit_code = validate_spec(spec_path.resolve())
    raise SystemExit(exit_code)


@main.command()
def version() -> None:
    """Print the installed version."""
    click.echo(__version__)


if __name__ == "__main__":
    main()
```

### 6.3 `src/dbt_specify/init.py`

```python
"""Implementation of `dbt-specify init`."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import click

from dbt_specify.templates_loader import asset_dir


def init_project(
    project_name: str,
    warehouse: str,
    target_dir: Path,
    force: bool,
) -> None:
    """Initialize a .dbt-specify/ directory in an existing dbt project.

    Args:
        project_name: Human-readable name for the project (logged, not enforced).
        warehouse: One of "snowflake", "databricks", or "trino".
        target_dir: Where to write the .dbt-specify/ directory.
        force: If True, overwrite existing .dbt-specify/.

    Raises:
        SystemExit: On any precondition failure.
    """
    if warehouse not in {"snowflake", "databricks", "trino"}:
        click.echo(f"error: unknown warehouse '{warehouse}'", err=True)
        raise SystemExit(2)

    dbt_project_yml = target_dir / "dbt_project.yml"
    if not dbt_project_yml.exists():
        click.echo(
            f"error: no dbt_project.yml found at {target_dir}.\n"
            f"  dbt-specify init must be run inside an existing dbt project.\n"
            f"  see docs/getting-started.md for help.",
            err=True,
        )
        raise SystemExit(1)

    specify_dir = target_dir / ".dbt-specify"
    if specify_dir.exists():
        if not force:
            click.echo(
                f"error: {specify_dir} already exists.\n"
                f"  re-run with --force to overwrite.",
                err=True,
            )
            raise SystemExit(1)
        shutil.rmtree(specify_dir)

    specify_dir.mkdir(parents=True, exist_ok=False)

    # 1. Copy base constitution
    _copy_file(
        src=asset_dir("memory") / "constitution.md",
        dst=specify_dir / "constitution.md",
    )

    # 2. Append warehouse-specific additions to the constitution
    additions = (asset_dir("presets") / warehouse / "constitution-additions.md").read_text()
    base_constitution = (specify_dir / "constitution.md").read_text()
    (specify_dir / "constitution.md").write_text(
        base_constitution
        + f"\n\n<!-- BEGIN {warehouse.upper()} ADDITIONS -->\n\n"
        + additions
        + f"\n\n<!-- END {warehouse.upper()} ADDITIONS -->\n"
    )

    # 3. Copy templates
    templates_dst = specify_dir / "templates"
    shutil.copytree(asset_dir("templates"), templates_dst)

    # 4. Append warehouse-specific plan additions to plan-template
    plan_additions = (asset_dir("presets") / warehouse / "plan-additions.md").read_text()
    plan_path = templates_dst / "plan-template.md"
    plan_path.write_text(
        plan_path.read_text()
        + f"\n\n<!-- BEGIN {warehouse.upper()} PLAN ADDITIONS -->\n\n"
        + plan_additions
        + f"\n\n<!-- END {warehouse.upper()} PLAN ADDITIONS -->\n"
    )

    # 5. Copy skills
    skills_dst = specify_dir / "skills"
    shutil.copytree(asset_dir("skills"), skills_dst)

    # 6. Copy warehouse-specific skills
    warehouse_skills_src = asset_dir("presets") / warehouse / "skills"
    if warehouse_skills_src.exists():
        for skill_dir in warehouse_skills_src.iterdir():
            if skill_dir.is_dir():
                shutil.copytree(skill_dir, skills_dst / skill_dir.name)

    # 7. Copy commands
    commands_dst = specify_dir / "commands"
    shutil.copytree(asset_dir("commands"), commands_dst)

    # 8. Create or suggest CLAUDE.md
    claude_template = (asset_dir("templates") / "CLAUDE.md.template").read_text().replace(
        "{{ project_name }}", project_name
    ).replace("{{ warehouse }}", warehouse)

    claude_target = target_dir / "CLAUDE.md"
    if claude_target.exists():
        suggested = target_dir / "CLAUDE.md.dbt-specify-suggested"
        suggested.write_text(claude_template)
        click.echo(
            f"note: {claude_target.name} already exists.\n"
            f"  wrote a suggested merge to {suggested.name} — review and integrate manually."
        )
    else:
        claude_target.write_text(claude_template)
        click.echo(f"wrote {claude_target.name}")

    # 9. Create empty specs/ directory for the user's first spec
    (target_dir / "specs").mkdir(exist_ok=True)
    (target_dir / "specs" / ".gitkeep").touch()

    click.echo(f"\ndbt-specify initialized in {target_dir}")
    click.echo(f"  warehouse preset: {warehouse}")
    click.echo(f"  next: see {target_dir}/.dbt-specify/constitution.md and {target_dir}/CLAUDE.md")


def _copy_file(src: Path, dst: Path) -> None:
    """Copy a single file, creating parent dirs if needed."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
```

### 6.4 `src/dbt_specify/validate.py`

```python
"""Implementation of `dbt-specify validate`."""
from __future__ import annotations

import re
from pathlib import Path

import click

from dbt_specify.ears import classify_ears


# Headers that mark the Acceptance Criteria section. Case-insensitive.
AC_SECTION_PATTERNS = [
    re.compile(r"^##+\s*acceptance\s+criteria\b", re.IGNORECASE),
    re.compile(r"^##+\s*ACs?\b", re.IGNORECASE),
]


def validate_spec(spec_path: Path) -> int:
    """Validate that a spec's Acceptance Criteria section is EARS-conformant.

    Args:
        spec_path: Path to a spec.md file.

    Returns:
        0 if all ACs conform to an EARS pattern, 1 otherwise.
    """
    text = spec_path.read_text()
    ac_lines = _extract_ac_lines(text)

    if not ac_lines:
        click.echo(
            f"warning: no Acceptance Criteria section found in {spec_path.name}",
            err=True,
        )
        return 1

    failures: list[tuple[int, str]] = []
    for line_no, line in ac_lines:
        pattern = classify_ears(line)
        if pattern is None:
            failures.append((line_no, line))

    if failures:
        click.echo(f"\n{len(failures)} AC line(s) do not match an EARS pattern:")
        for line_no, line in failures:
            click.echo(f"  line {line_no}: {line.strip()}")
        click.echo(
            "\nsee docs/ears-cheatsheet.md for the five EARS patterns and dbt examples."
        )
        return 1

    click.echo(f"ok: {len(ac_lines)} AC line(s) all match an EARS pattern.")
    return 0


def _extract_ac_lines(text: str) -> list[tuple[int, str]]:
    """Find lines that look like ACs inside the Acceptance Criteria section."""
    lines = text.splitlines()
    in_ac_section = False
    next_section = re.compile(r"^##+\s+", re.IGNORECASE)
    ac_lines: list[tuple[int, str]] = []

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if any(p.match(stripped) for p in AC_SECTION_PATTERNS):
            in_ac_section = True
            continue
        if in_ac_section and next_section.match(stripped):
            # We hit the next ## section, so we're done with ACs.
            break
        if in_ac_section:
            # Treat any non-empty line that doesn't start with a markdown decoration
            # as a potential AC line. Bullet markers and AC labels are stripped.
            cleaned = _clean_ac_line(stripped)
            if cleaned:
                ac_lines.append((i, cleaned))

    return ac_lines


def _clean_ac_line(line: str) -> str:
    """Strip bullets, AC prefixes, and bold/italic markers."""
    # Strip leading list markers
    line = re.sub(r"^[-*+]\s+", "", line)
    # Strip AC labels like "AC1:", "**AC1**:", "AC1 —", etc.
    line = re.sub(r"^\**AC\d*\**\s*[:\-—]\s*", "", line, flags=re.IGNORECASE)
    # Strip EARS-pattern labels like "(Ubiquitous)" or "**(Event-driven)**"
    line = re.sub(r"^\**\([^)]+\)\**\s*[—-]?\s*", "", line)
    return line.strip()
```

### 6.5 `src/dbt_specify/ears.py`

```python
"""EARS pattern classification.

EARS = Easy Approach to Requirements Syntax. Five patterns:

  1. Ubiquitous:    "The system shall <response>."
  2. Event-driven:  "When <trigger>, the system shall <response>."
  3. State-driven:  "While <state>, the system shall <response>."
  4. Unwanted:      "If <unwanted>, then the system shall <response>."
  5. Optional:      "Where <feature>, the system shall <response>."

We use loose matching — the requirement phrasing must contain the right
trigger keyword *and* the "shall" verb. Punctuation and capitalization
are tolerant.
"""
from __future__ import annotations

import re

# All patterns require " shall " or " must " somewhere after the trigger.
_RESPONSE_VERB = r"(shall|must)"


# Order matters: more specific (Event/State/Unwanted/Optional) before Ubiquitous.
_PATTERNS = [
    ("event_driven", re.compile(rf"^\s*when\b.*?,?\s*the\s+system\s+{_RESPONSE_VERB}\b", re.IGNORECASE | re.DOTALL)),
    ("state_driven", re.compile(rf"^\s*while\b.*?,?\s*the\s+system\s+{_RESPONSE_VERB}\b", re.IGNORECASE | re.DOTALL)),
    ("unwanted",     re.compile(rf"^\s*if\b.*?,?\s*then\s+the\s+system\s+{_RESPONSE_VERB}\b", re.IGNORECASE | re.DOTALL)),
    ("optional",     re.compile(rf"^\s*where\b.*?,?\s*the\s+system\s+{_RESPONSE_VERB}\b", re.IGNORECASE | re.DOTALL)),
    ("ubiquitous",   re.compile(rf"^\s*the\s+system\s+{_RESPONSE_VERB}\b", re.IGNORECASE | re.DOTALL)),
]


def classify_ears(line: str) -> str | None:
    """Return the EARS pattern name for a given line, or None if not EARS.

    >>> classify_ears("The system shall ship a CLI.")
    'ubiquitous'
    >>> classify_ears("When init is invoked, the system shall create .dbt-specify/.")
    'event_driven'
    >>> classify_ears("Hello world")
    """
    for name, pattern in _PATTERNS:
        if pattern.search(line):
            return name
    return None
```

### 6.6 `src/dbt_specify/templates_loader.py`

```python
"""Load packaged template assets from the installed dbt-specify package."""
from __future__ import annotations

from functools import lru_cache
from importlib import resources
from pathlib import Path


@lru_cache(maxsize=None)
def asset_dir(kind: str) -> Path:
    """Return the on-disk path to a packaged asset directory.

    Args:
        kind: One of "memory", "templates", "presets", "skills", "commands".

    Returns:
        Absolute Path to the directory inside the installed package.

    Raises:
        ValueError: If `kind` is not a known asset directory.
    """
    if kind not in {"memory", "templates", "presets", "skills", "commands"}:
        raise ValueError(f"unknown asset kind: {kind}")

    # We use importlib.resources for proper package-data discovery.
    package_files = resources.files("dbt_specify") / "_assets" / kind
    # files() returns a Traversable; convert to Path for shutil compatibility.
    return Path(str(package_files))


def load_template(name: str) -> str:
    """Read a top-level template file.

    Args:
        name: Template name without extension (e.g., "spec" loads spec-template.md).

    Returns:
        The template content as a string.
    """
    candidates = [
        asset_dir("templates") / f"{name}-template.md",
        asset_dir("templates") / f"{name}.md",
        asset_dir("templates") / name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.read_text()
    raise FileNotFoundError(f"no template found for name '{name}'")
```

### 6.7 Test structure

**`tests/conftest.py`:**

```python
"""Shared pytest fixtures."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def minimal_dbt_project(tmp_path: Path) -> Path:
    """Create a minimal dbt project directory and return its path."""
    project_dir = tmp_path / "dbt_proj"
    project_dir.mkdir()
    (project_dir / "dbt_project.yml").write_text(
        "name: test_project\nversion: '1.0.0'\nprofile: test\n"
    )
    (project_dir / "models").mkdir()
    return project_dir
```

**`tests/test_init.py` skeleton:**

```python
"""Tests for the init command."""
from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from dbt_specify.cli import main


def test_init_creates_dbt_specify_dir(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0, result.output
    assert (minimal_dbt_project / ".dbt-specify").is_dir()
    assert (minimal_dbt_project / ".dbt-specify" / "constitution.md").exists()


def test_init_appends_snowflake_additions(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    constitution = (minimal_dbt_project / ".dbt-specify" / "constitution.md").read_text()
    assert "BEGIN SNOWFLAKE ADDITIONS" in constitution
    assert "clustering" in constitution.lower()


def test_init_fails_without_dbt_project_yml(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(tmp_path)],
    )
    assert result.exit_code != 0
    assert "dbt_project.yml" in result.output


def test_init_refuses_to_overwrite_without_force(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "snowflake", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code != 0
    assert "already exists" in result.output


def test_init_databricks_preset(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "databricks", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0
    constitution = (minimal_dbt_project / ".dbt-specify" / "constitution.md").read_text()
    assert "BEGIN DATABRICKS ADDITIONS" in constitution
    assert "liquid clustering" in constitution.lower()


def test_init_trino_preset(minimal_dbt_project: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["init", "test", "--warehouse", "trino", "--target", str(minimal_dbt_project)],
    )
    assert result.exit_code == 0
    constitution = (minimal_dbt_project / ".dbt-specify" / "constitution.md").read_text()
    assert "BEGIN TRINO ADDITIONS" in constitution
    # Trino is a federated query engine — that word should appear in the additions.
    assert "federation" in constitution.lower() or "federated" in constitution.lower()
```

**`tests/test_ears.py` skeleton:**

```python
"""Tests for EARS pattern classification."""
from __future__ import annotations

import pytest

from dbt_specify.ears import classify_ears


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("The system shall ship a CLI.", "ubiquitous"),
        ("the system must support snowflake", "ubiquitous"),
        ("When init is invoked, the system shall create .dbt-specify/.", "event_driven"),
        ("While in plan mode, the system shall not write code.", "state_driven"),
        ("If no dbt_project.yml exists, then the system shall exit non-zero.", "unwanted"),
        ("Where Snowflake is selected, the system shall add clustering hints.", "optional"),
    ],
)
def test_classify_ears_positive(line: str, expected: str) -> None:
    assert classify_ears(line) == expected


@pytest.mark.parametrize(
    "line",
    [
        "Hello world",
        "We should probably build a CLI",
        "Init creates .dbt-specify/",
        "The system would maybe support snowflake",
    ],
)
def test_classify_ears_negative(line: str) -> None:
    assert classify_ears(line) is None
```

**`tests/test_validate.py` skeleton:**

```python
"""Tests for the validate command."""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from dbt_specify.cli import main


def test_validate_accepts_ears_spec(tmp_path: Path) -> None:
    spec = tmp_path / "spec.md"
    spec.write_text(
        "# Test spec\n\n"
        "## Acceptance criteria\n\n"
        "- AC1: The system shall ship a CLI.\n"
        "- AC2: When init runs, the system shall create .dbt-specify/.\n"
    )
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(spec)])
    assert result.exit_code == 0


def test_validate_rejects_non_ears_spec(tmp_path: Path) -> None:
    spec = tmp_path / "spec.md"
    spec.write_text(
        "# Test spec\n\n"
        "## Acceptance criteria\n\n"
        "- We want a CLI.\n"
        "- It should create .dbt-specify/ sometimes.\n"
    )
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(spec)])
    assert result.exit_code != 0
    assert "do not match" in result.output
```

**Fixtures** — `tests/fixtures/valid_spec.md`:

```markdown
# Sample valid spec

## Acceptance criteria

- AC1: The system shall ship a working CLI.
- AC2: When the user runs init, the system shall create the target directory.
- AC3: If the dbt_project.yml is missing, then the system shall exit non-zero.
```

**Fixtures** — `tests/fixtures/invalid_spec_non_ears.md`:

```markdown
# Sample invalid spec

## Acceptance criteria

- We want a CLI.
- It should probably work.
- AC3: The dbt_project.yml is required.
```

### 6.8 `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"
      - name: Lint
        run: ruff check src tests
      - name: Type-check
        run: mypy src
      - name: Test
        run: pytest
```

---

## 7. README and supporting top-level docs

### 7.1 `README.md`

```markdown
# dbt-spec-kit

> Spec-driven development for dbt — with warehouse-specific presets for Snowflake, Databricks, and Trino.

Modeled on [github/spec-kit](https://github.com/github/spec-kit). Composes with [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills). Works with Claude Code, Cursor, GitHub Copilot, Gemini CLI, Cline, and any agent that reads markdown context.

## Why this exists

AI coding agents are powerful but vague. "Build a customer mart" gets you wildly different output depending on agent context. dbt-spec-kit fixes that by making **specs the source of truth**: written once, agent-readable, warehouse-aware.

Four phases, one human checkpoint per phase, never auto-merge.

```
Specify  →  Plan  →  Tasks  →  Implement
   ↑                                |
   └──────────  retro  ←────────────┘
```

## Install

Requires Python 3.11+. Recommended via [uv](https://docs.astral.sh/uv/):

```bash
uvx --from git+https://github.com/duckcode-ai/dbt-spec-kit.git dbt-specify init my-project --warehouse snowflake
```

Or persistent install:

```bash
uv tool install dbt-spec-kit --from git+https://github.com/duckcode-ai/dbt-spec-kit.git
dbt-specify init my-project --warehouse snowflake
```

## What you get

Running `init` in your existing dbt project creates:

- `.dbt-specify/constitution.md` — the project's non-negotiable principles (base + warehouse-specific additions)
- `.dbt-specify/templates/` — spec, plan, tasks, retro templates
- `.dbt-specify/skills/` — tier-2 and tier-3 skills for writing specs
- `.dbt-specify/commands/` — slash-command prompts (`/dbt.specify`, `/dbt.plan`, `/dbt.tasks`, `/dbt.implement`)
- `CLAUDE.md` — references the constitution, defers tier-1 questions to `dbt-labs/dbt-agent-skills`
- `specs/` — empty directory for your first spec

## The three positioning pillars

| Pillar | What we ship |
|---|---|
| Methodology layer | Constitution + four-phase templates + CLI |
| Warehouse presets | Snowflake (clustering, warehouse sizing, query tags, masking), Databricks (Liquid Clustering, Photon, Unity Catalog), and Trino (federation patterns, catalog discipline, connector pushdown) |
| Tier-3 skills | The one nobody else ships — writing business glossary and entity-resolution specs |

## What this is not

- **Not a replacement** for `dbt-labs/dbt-agent-skills`. Install both. They compose.
- **Not an IDE.** Markdown templates and a thin CLI. Bring your own agent.
- **Not opinionated about agents.** Works with anything that reads markdown context.

## Worked example

See [`examples/jaffle-shop-staging-overhaul/`](examples/jaffle-shop-staging-overhaul/) for a complete spec → plan → tasks → implementation trace.

## Docs

- [Getting started](docs/getting-started.md) — install + your first spec in 5 minutes
- [Methodology](docs/methodology.md) — the four-phase loop in depth
- [EARS cheatsheet](docs/ears-cheatsheet.md) — the five testable spec patterns with dbt examples
- [Snowflake guide](docs/warehouse-guides/snowflake.md)
- [Databricks guide](docs/warehouse-guides/databricks.md)
- [Trino guide](docs/warehouse-guides/trino.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The most useful contributions today: a BigQuery preset, more tier-3 skills, real-world worked examples from your project.

## License

MIT.
```

### 7.2 `CHANGELOG.md`

```markdown
# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — <YYYY-MM-DD>

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
```

### 7.3 `CONTRIBUTING.md`

```markdown
# Contributing to dbt-spec-kit

Thanks for considering a contribution. This project is small on purpose — the most useful contributions are:

1. **A new warehouse preset** (BigQuery, Redshift, or any other modern adapter). Follow the structure in `presets/snowflake/` (or `presets/trino/` if your target is more like a federated query engine than a warehouse).
2. **A tier-3 skill** for a specific data domain. See `skills/writing-business-glossary-specs/SKILL.md` for the pattern.
3. **A real-world worked example** from your dbt project, anonymized.
4. **Bug fixes** to the EARS validator (especially false positives on valid specs).

## Local setup

```bash
git clone https://github.com/duckcode-ai/dbt-spec-kit
cd dbt-spec-kit
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
```

All three must pass before opening a PR.

## How to add a warehouse preset

1. Create `presets/<warehouse>/constitution-additions.md`. Append-only — do not repeal base principles.
2. Create `presets/<warehouse>/plan-additions.md`. Add sections to the plan template for warehouse-specific concerns (clustering, governance, cost monitoring, etc.).
3. Add at least one warehouse-specific skill under `presets/<warehouse>/skills/`.
4. Add `--warehouse <name>` to the CLI's `Click.Choice` in `src/dbt_specify/cli.py`.
5. Add a test case mirroring `test_init_databricks_preset`.

## How to write a tier-3 skill

Tier-3 means **business domain context** — not framework conventions (tier 1, owned by dbt-labs/dbt-agent-skills) and not team conventions (tier 2, owned by each project). Tier-3 captures *what your business actually is* — entity definitions, grain decisions, cross-system identifier resolution.

The pattern:
1. Start with a one-paragraph problem statement (a real situation where this context matters).
2. Provide a structured template the user fills in.
3. Give one fully-worked example.
4. List 3–5 anti-patterns to avoid.

See `skills/writing-business-glossary-specs/SKILL.md` for the reference implementation.

## Coding conventions

- Python 3.11+ with type hints everywhere
- `ruff check src tests` and `mypy src` both green before PR
- Sentence-case headers in markdown, no emoji in templates
- New tests for every behavior change

## License

By contributing, you agree your contributions are licensed under MIT (same as the project).
```

---

## 8. Content appendix — every markdown file in full

### 8.1 `memory/constitution.md` (the base, warehouse-agnostic constitution)

```markdown
# dbt project constitution

<!-- INSTRUCTIONS: This is the non-negotiable rulebook for an AI agent working on this dbt project. Every spec, plan, task, and implementation must respect these articles. Articles below the BEGIN ADDITIONS marker are warehouse-specific. -->

## Article 1 — Spec-first

No code is written before a spec is approved. The spec lives at `specs/<NNN>-<slug>/spec.md` and includes acceptance criteria in EARS format.

## Article 2 — Plan-then-implement

No code is written before a plan is approved. The plan lives at `specs/<NNN>-<slug>/plan.md` and lists every file that will be added, modified, or deleted.

## Article 3 — Human approval at each phase

A human engineer must explicitly approve the spec before planning, the plan before tasks, and the final diff before merge. AI never approves its own work.

## Article 4 — Tests are part of the work

Every model must have at least one test. Every transformation with business logic must have at least one unit test (`dbt test`-compatible unit tests, not just generic schema tests). Coverage on changed files is part of the merge bar.

## Article 5 — Grain is explicit

Every model declares its grain in a YAML doc comment. Mart-level models declare grain in the spec itself. "What is one row in this table?" must be answerable in one sentence.

## Article 6 — Source contracts are explicit

Every source is declared in `sources.yml` with `freshness`, `loaded_at_field`, and at least basic schema tests. Specs reference sources by their qualified name (`source.<name>.<table>`), not raw warehouse names.

## Article 7 — Semantic layer alignment

If a model is consumed by the semantic layer, the spec calls out which metrics and dimensions it serves. Breaking changes to semantic-layer-consumed models require a metric impact analysis in the plan.

## Article 8 — Exposures are first-class

If a model powers a dashboard, a reverse-ETL pipeline, or an API, it has a matching `exposure` entry. The plan checks downstream exposures and the implementation summary lists which exposures were affected.

## Article 9 — Naming conventions are enforced, not suggested

Staging models: `stg_<source>__<entity>.sql`. Intermediate: `int_<entity>_<purpose>.sql`. Marts: `dim_<entity>.sql` (dimension) or `fct_<process>.sql` (fact). Snapshot: `snp_<entity>.sql`. Specs that propose names violating this rule are rejected during plan review.

## Article 10 — Convention over configuration

When dbt offers multiple ways to do something, the project picks one and sticks to it. Examples: materialization choice (incremental vs. table for fact tables), test placement (in `schema.yml` vs. singular tests), macro location (`macros/` vs. inline Jinja). The convention is captured in CLAUDE.md.

## Article 11 — No silent breaking changes

A change is "breaking" if any downstream model, exposure, or semantic-layer metric would need to update. Breaking changes require: (a) explicit call-out in the spec, (b) a migration plan in the plan.md, (c) communication to affected consumers documented in the implementation summary.

## Article 12 — Retro is not optional

After every shipped feature, a retro is written to `specs/<NNN>-<slug>/retro.md` or appended to the implementation summary. The retro must answer: did the agent need clearer instructions anywhere? Did any convention need updating? Was a skill missing? Updates to CLAUDE.md or skills are filed as a separate PR.

## Article 13 — Composition with dbt-labs/dbt-agent-skills

Questions about "how does dbt work" (running tests, debugging failures, semantic layer setup, dbt Mesh) defer to `dbt-labs/dbt-agent-skills`. This constitution covers what to build and how this team builds it, not the dbt framework itself.
```

### 8.2 `templates/spec-template.md`

```markdown
<!-- INSTRUCTIONS:
  Fill in every section below. Acceptance criteria MUST be in EARS format:
    - Ubiquitous:    "The system shall <response>."
    - Event-driven:  "When <trigger>, the system shall <response>."
    - State-driven:  "While <state>, the system shall <response>."
    - Unwanted:      "If <unwanted>, then the system shall <response>."
    - Optional:      "Where <feature>, the system shall <response>."
  Run `dbt-specify validate path/to/this/spec.md` to check EARS conformance.
  Remove this INSTRUCTIONS block before merging — or leave it; future iterations benefit.
-->

# <feature title>

**Ticket:** <project tracker id>
**Author:** <name>
**Date:** <YYYY-MM-DD>
**Status:** draft | approved | shipped

## Problem

<One paragraph. What's broken or missing. Who's affected. Why now.>

## Users

<Who this is for and the job they're hiring it for. One row per user type.>

| User | Job to be done |
|---|---|
| <persona> | <one-sentence job> |

## What this is

<2–4 sentences. The result of this work, in plain language. No tech stack details — those go in the plan.>

## Acceptance criteria

<!-- Each AC is one line. Each line uses an EARS pattern. -->

- AC1: <ubiquitous AC>
- AC2: <event-driven AC>
- AC3: <unwanted-condition AC>

## Out of scope

<What this does NOT do. Be specific — vague out-of-scope sections are common spec failure modes.>

- <thing we are not doing>
- <thing someone might assume but we are not doing>

## Constraints

- Warehouse: <snowflake|databricks|other>
- Materialization: <table|view|incremental|...>
- Grain: <one sentence — what is one row?>
- Refresh cadence: <hourly|daily|on-demand>
- Downstream consumers: <semantic layer metrics, dashboards, reverse-ETL, ML features>

## Open questions

<Things the spec doesn't decide yet. Resolve before plan phase.>

- [ ] <question>
```

### 8.3 `templates/plan-template.md`

```markdown
<!-- INSTRUCTIONS:
  This plan is approved BEFORE any code is written.
  List every file that will be added, modified, or deleted.
  Call out warehouse-specific concerns in the warehouse sections (Snowflake/Databricks).
-->

# Plan — <feature title>

**Spec:** ../spec.md
**Author:** <agent name + reviewer>
**Date:** <YYYY-MM-DD>
**Status:** proposed | approved | superseded

## Architecture

<2–4 sentences. The shape of the solution. Reference any relevant constitution articles.>

## Files to add

| Path | Purpose |
|---|---|
| `models/staging/<source>/stg_<source>__<entity>.sql` | <purpose> |
| `models/staging/<source>/_<source>__sources.yml` | source declarations |
| `models/staging/<source>/_<source>__models.yml` | staging schema + tests |

## Files to modify

| Path | Change |
|---|---|
| <path> | <one-line change description> |

## Files to delete

<Empty unless the change removes models. List explicitly — silent deletes are a Constitution §11 violation.>

| Path | Reason |
|---|---|
| <path> | <why this is safe to remove> |

## Tests

<List the tests this plan will produce. Reference each AC.>

| Test | AC covered |
|---|---|
| `unique` and `not_null` on `stg_<source>__<entity>.<grain>` | AC2 |
| Unit test: <scenario> | AC3 |

## Risks

<Warehouse-agnostic risks. Warehouse-specific risks go in the warehouse section below.>

| Risk | Mitigation |
|---|---|
| <risk> | <mitigation> |

## Downstream impact

| Consumer | Impact | Notification |
|---|---|---|
| Semantic-layer metric `<metric>` | <none|breaking|additive> | <who/when> |
| Exposure `<exposure>` | <none|breaking|additive> | <who/when> |
| Reverse-ETL `<destination>` | <none|breaking|additive> | <who/when> |

## Open questions for review

- [ ] <question for the human reviewer>
```

### 8.4 `templates/tasks-template.md`

```markdown
<!-- INSTRUCTIONS:
  This is the work breakdown. Each task is small enough to commit in one PR.
  Tasks are ordered: dependencies first, leaf work last.
  Each task lists its definition of done.
-->

# Tasks — <feature title>

**Plan:** ../plan.md
**Status:** in progress | done

## Task list

- [ ] **T-01** — <imperative task description>
  - **Done when:** <observable criterion>
  - **Validates:** AC<N>

- [ ] **T-02** — ...

## Test plan

<How we'll verify the whole feature, not just individual tasks.>

- [ ] `dbt build --select +<final_model>+` runs green locally
- [ ] `dbt test` passes for all changed models
- [ ] Unit tests for AC3 and AC4 are present
- [ ] Downstream exposures still resolve

## Done definition

<The whole feature is done when:>

- [ ] All tasks above are checked
- [ ] All ACs are verified
- [ ] Plan's downstream-impact actions have been completed
- [ ] Retro is filed (see retro-template.md)
```

### 8.5 `templates/retro-template.md`

```markdown
<!-- INSTRUCTIONS:
  Write this after the feature ships. Focus on the routine, not the work itself.
  The goal is to make the next ticket start in a better place.
-->

# Retro — <feature title>

**Date shipped:** <YYYY-MM-DD>
**Lead time (spec to prod):** <duration>

## What went well

- <observation about the routine that worked>

## What to change for next time

- <CLAUDE.md update, new skill, new convention>

## Updates filed

- [ ] CLAUDE.md change: <PR link>
- [ ] New skill: <PR link>
- [ ] Eval fixture: <PR link>

## Metrics

| Metric | Value |
|---|---|
| Plan-phase time | <duration> |
| Implement-phase time | <duration> |
| AI review findings | <count> (<count fixed pre-merge>) |
| Human review findings | <count> |
| Post-merge issues | <count> |
```

### 8.6 `templates/CLAUDE.md.template`

```markdown
# CLAUDE.md — {{ project_name }}

This file orients AI coding agents (Claude Code, Cursor, Copilot, Gemini CLI, Cline, etc.) to this dbt project's conventions and workflow.

## Project type

dbt project, warehouse: **{{ warehouse }}**.

## Workflow

This project follows the four-phase loop from [dbt-spec-kit](https://github.com/duckcode-ai/dbt-spec-kit):

1. **Specify** — `specs/<NNN>-<slug>/spec.md` is approved before planning.
2. **Plan** — `specs/<NNN>-<slug>/plan.md` is approved before code.
3. **Tasks** — `specs/<NNN>-<slug>/tasks.md` is the ordered work breakdown.
4. **Implement** — code follows the plan exactly.

After ship, write a retro to the same spec directory.

## Slash commands

Four commands map to the phases:

- `/dbt.specify <feature description>` — drafts a spec from a prompt
- `/dbt.plan` — reads the current spec and proposes a plan
- `/dbt.tasks` — decomposes the approved plan into ordered tasks
- `/dbt.implement` — executes the next task

See `.dbt-specify/commands/` for the prompts.

## Constitution

The non-negotiable principles for this project are in `.dbt-specify/constitution.md`. Read them before writing any spec or plan.

## Where context lives

| Question | Where to find the answer |
|---|---|
| How does dbt work? (running tests, debugging, semantic layer mechanics) | [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills) — install separately |
| How does THIS project structure models / name things / handle CTE patterns? | This file + `.dbt-specify/constitution.md` |
| What does the business actually mean by "customer" / "order" / "session"? | `.dbt-specify/skills/writing-business-glossary-specs/SKILL.md` — fill in your glossary spec |
| What are {{ warehouse }}-specific patterns we follow here? | `.dbt-specify/constitution.md` (BEGIN {{ warehouse }} ADDITIONS section) |

## Conventions specific to this project

<!-- Add your team's specific conventions here. Examples:
  - Staging models always use a 5-CTE pattern: source → renamed → filtered → enhanced → final
  - All staging models include surrogate keys via dbt_utils.generate_surrogate_key
  - We never use `*` in select statements outside the source CTE
  - All masks/PII handling is in the staging layer, never marts
-->

(Fill in your team's conventions here.)

## How AI agents should behave on this project

- Always read `.dbt-specify/constitution.md` first.
- Never skip a phase. Always produce a spec, then a plan, then tasks, before code.
- Surface drift, don't fix it silently. If you notice a convention is being broken or a deprecated pattern is being used elsewhere, write it to `specs/<current>/findings.md` — do not edit unrelated files.
- All proposed changes must trace to an AC in the spec.
```

### 8.7 `presets/snowflake/constitution-additions.md`

```markdown
## Article S1 — Clustering keys are explicit decisions

Tables larger than 1 GB declare a clustering key in `config(cluster_by=[...])`. The choice of clustering key is justified in the plan. Tables smaller than 1 GB do not need clustering.

## Article S2 — Warehouse sizing is documented

Production builds use a named warehouse. The spec or plan declares which warehouse and at what size (X-Small, Small, Medium, ...). Auto-suspend is set to ≤ 5 minutes.

## Article S3 — Query tags are required

All production runs set `query_tag` via a `dbt_project.yml` pre-hook so spend can be attributed by team and project. The query tag includes at minimum: project name, model name, environment (dev|prod), and invocation id.

## Article S4 — Masking and row access policies

Any column carrying PII or restricted data is masked via a Snowflake masking policy attached at the table level. Masking policies live in `models/_governance/masking_policies.sql` and are tested for correctness via dbt unit tests.

## Article S5 — Dynamic tables, when used, are first-class

If a model is materialized as a Snowflake dynamic table, the spec calls out: target lag, refresh mode (incremental vs. full), and downstream dependencies. Dynamic tables are NOT the default — explicit choice required.

## Article S6 — Cortex usage is governed

LLM-powered transformations (Cortex `COMPLETE`, `SUMMARIZE`, etc.) are: (a) called out in the spec, (b) tested with deterministic fixtures, (c) cost-capped via warehouse sizing. No Cortex calls outside `models/_ai/` without an explicit waiver in the plan.
```

### 8.8 `presets/snowflake/plan-additions.md`

```markdown
## Snowflake-specific concerns

### Clustering decisions

| Model | Size estimate | Clustering key | Justification |
|---|---|---|---|
| <model> | <GB> | `[col1, col2]` or none | <why> |

### Warehouse sizing

| Job | Warehouse | Size | Auto-suspend (s) | Justification |
|---|---|---|---|---|
| <job> | <wh_name> | <size> | <s> | <why> |

### Query tag plan

The `query_tag` for this work will include: `project=<project>, model=<model>, env=<env>, run_id=<run_id>`.

### Masking & governance

| Column | Source | Policy | Tested? |
|---|---|---|---|
| <col> | <source.table.col> | <policy_name> | yes/no |

### Cost guardrails

| Risk | Mitigation |
|---|---|
| Unbounded scan on large source | Add date predicate via incremental config |
| Unintended warehouse upsize | Use named warehouse, not USE WAREHOUSE inline |
```

### 8.9 `presets/snowflake/skills/snowflake-clustering-decisions/SKILL.md`

```markdown
---
name: snowflake-clustering-decisions
description: Use when deciding whether and how to add a clustering key to a Snowflake-backed dbt model.
---

# Choosing clustering keys for Snowflake dbt models

## When to use this skill

You're proposing a new model or modifying an existing one, and need to decide whether to add `config(cluster_by=[...])`. Use this skill to make the decision deliberately rather than by reflex.

## The decision rules

**Add a clustering key if all of these are true:**
1. The table will exceed 1 GB compressed (estimate from source row count × avg row size).
2. The most common query predicates include a column with high cardinality and natural temporal/categorical ordering (often `event_date`, `customer_id`, `region`).
3. The table is queried more often than rebuilt. (Clustering costs reorganization on insert.)

**Skip clustering if any of these are true:**
1. Table is < 1 GB compressed.
2. Table is rebuilt full every run (clustering is wasted).
3. Predicates are unpredictable (e.g., ad-hoc analytics tables).

## How to pick the key

- One column is usually better than three. Snowflake docs say up to 4, but maintenance cost rises sharply.
- Prefer the column most often used in `WHERE` and `JOIN`.
- For event/fact tables, `event_date` (or a derived `event_month` for very large tables) is the conventional choice.
- For wide dimension tables, the natural primary join key is usually right.

## How to verify the choice

After the model is built, run a representative query and check the `Partitions scanned` vs. `Partitions total` in the query profile. A well-clustered table scans <10% of partitions for selective predicates.

```sql
-- example: check clustering health on a real query
SELECT system$clustering_information('analytics.fct_orders', 'order_date');
```

## Anti-patterns

- **Clustering on `created_at` when queries filter on `event_date`** — keys must match query patterns, not row insertion patterns.
- **Clustering tables under 1 GB** — adds maintenance overhead with no scan benefit.
- **Clustering on a surrogate key** — high cardinality but rarely used in `WHERE`; usually wrong.
- **Three-column clustering on a small dimension** — premature optimization.

## In the spec/plan

The plan's "Clustering decisions" table should justify the choice for each table >1 GB. Reviewers check the justification, not just that a key is present.
```

### 8.10 `presets/databricks/constitution-additions.md`

```markdown
## Article D1 — Liquid Clustering, not partitioning

New tables use Liquid Clustering (`CLUSTER BY (col)`), not rigid partition columns. The clustering column is declared in `config(liquid_clustered_by=[...])`. Tables migrated from partitioning to Liquid Clustering call out the migration in the plan.

## Article D2 — Photon is the default execution engine

Production warehouses use Photon. The spec or plan calls out any model that *must* run on classic compute (e.g., uses a UDF Photon doesn't support).

## Article D3 — Unity Catalog is the governance layer

All models are addressed via three-part names: `<catalog>.<schema>.<model>`. Grants are declared in `_governance/grants.sql` and applied as post-hooks. Hive metastore is not used for new work.

## Article D4 — Materialized Views for incremental work

For incremental processing, prefer Materialized Views (`materialized='materialized_view'`) over hand-rolled incremental dbt models when the warehouse supports them. Specs that propose `materialized='incremental'` justify why an MV won't work.

## Article D5 — Query tags via system tables

Cost attribution uses Databricks query tags written to `system.access.audit`. The tag schema mirrors Snowflake's: `project`, `model`, `env`, `run_id`.

## Article D6 — AI/ML governance

LLM calls via `ai_query()` or Mosaic AI endpoints are: (a) called out in the spec, (b) tested with deterministic fixtures, (c) governed by per-endpoint cost limits.
```

### 8.11 `presets/databricks/plan-additions.md`

```markdown
## Databricks-specific concerns

### Liquid Clustering decisions

| Model | Size estimate | Clustering key | Justification |
|---|---|---|---|
| <model> | <GB> | `<col>` or none | <why> |

### Materialization choice

| Model | Materialization | Justification |
|---|---|---|
| <model> | view / table / materialized_view / streaming_table | <why this and not an MV> |

### Unity Catalog placement

| Model | Catalog | Schema | Grants |
|---|---|---|---|
| <model> | <catalog> | <schema> | `_governance/grants.sql` entry: <line ref> |

### Photon compatibility

| Model | Photon-compatible? | If no, why |
|---|---|---|
| <model> | yes / no | <reason> |

### Cost guardrails

| Risk | Mitigation |
|---|---|
| Predictive Optimization not enabled on changed tables | Verify via `DESCRIBE TABLE EXTENDED` after first build |
| Streaming Table without watermark | Plan declares watermark column explicitly |
```

### 8.12 `presets/databricks/skills/databricks-liquid-clustering-decisions/SKILL.md`

```markdown
---
name: databricks-liquid-clustering-decisions
description: Use when deciding the clustering column(s) for a Databricks-backed dbt model using Liquid Clustering.
---

# Choosing Liquid Clustering for Databricks dbt models

## When to use this skill

You're configuring a new table on Databricks via dbt and need to decide between: no clustering, Liquid Clustering, or (rarely now) classic partitioning.

## The decision rules

**Use Liquid Clustering if:**
1. Table will be queried with selective predicates on one or more columns.
2. You don't have perfect foresight on the access pattern (Liquid is more forgiving than partitioning).
3. Table will grow over time and write patterns may shift.

**Skip clustering if:**
1. Table is small (<1 GB) and queries are unselective.
2. Table is rebuilt full every run.

**Use classic partitioning only if:**
1. You have a strong, stable query predicate that aligns to a natural temporal column.
2. You're on a runtime that doesn't support Liquid Clustering yet.

## How to pick clustering columns

- Up to 4 columns supported; one is usually enough.
- Prefer columns frequently in `WHERE` and `JOIN` keys.
- High-cardinality columns benefit more than low-cardinality ones.
- For fact tables, `event_date` is a frequent winner. For wide dimensions, the natural surrogate key.

## How to verify

After build, check the table properties:

```sql
DESCRIBE TABLE EXTENDED <catalog>.<schema>.<table>;
-- look for clusteringColumns property
```

Run a representative selective query and check the Spark UI for files pruned.

## Anti-patterns

- **Clustering on every selectable column** — diminishing returns past 1–2 columns.
- **Liquid Clustering on a small reference table** — useless overhead.
- **Mixing classic partitioning and Liquid Clustering** — pick one per table.
- **Clustering on a column that's masked** — masking happens before clustering, so the clustering benefit disappears.

## Predictive Optimization

Liquid Clustering composes with Predictive Optimization. Verify PO is enabled at the schema level:

```sql
ALTER SCHEMA <catalog>.<schema> ENABLE PREDICTIVE OPTIMIZATION;
```

## In the spec/plan

The plan's "Liquid Clustering decisions" table justifies each clustering column. Reviewers check the justification matches the query pattern in the spec's "Constraints" section.
```

### 8.12a `presets/trino/constitution-additions.md`

**Important note for the implementer.** Trino is fundamentally different from Snowflake and Databricks — it's a federated query engine, not a warehouse. The constitution additions below are written with that framing. Do NOT just copy the Snowflake/Databricks structure and rename. The articles below are intentionally different in shape because Trino's concerns are different (catalogs, connectors, pushdown, federation), not just different in name.

```markdown
## Article T1 — Trino is a query engine, not a warehouse

Models built on Trino are not "stored in Trino." Storage lives in the underlying connector (Iceberg, Delta, Hive, Postgres, Kafka, etc.). Spec and plan documents declare both the **catalog** (= connector + storage) and any storage-format concerns for that catalog. Storage decisions (partitioning, file size, table format options) belong in plan-additions sections aligned to the catalog used.

## Article T2 — Three-part naming is mandatory

All references use three-part names: `<catalog>.<schema>.<table>`. Two-part references are forbidden, even when the default catalog is set. Reason: silent routing to the wrong catalog is one of the most common Trino-on-dbt failure modes, and three-part names make every cross-catalog join visible at code-review time.

## Article T3 — Cross-catalog joins are deliberate, never accidental

Any model that joins across two or more catalogs is called out in the spec's "Constraints" section AND in the plan's "Federation impact" table. Cross-catalog joins move data over the network and the cost model is opaque. Reviewers reject plans that introduce cross-catalog joins without explicit justification.

## Article T4 — Connector pushdown is a planning concern, not a runtime hope

For every model that filters or aggregates on a non-Iceberg-native catalog (Postgres, MySQL, Hive with Glue, Kafka), the plan declares **which predicates are expected to push down** and how this was verified (via `EXPLAIN`). Models that scan an entire underlying table because pushdown silently failed are a Constitution §11 violation (silent breaking change to performance contract).

## Article T5 — Session properties replace warehouse sizing

Trino has no equivalent of Snowflake's named warehouses or Databricks's compute clusters at the per-query level. Session properties (`query_max_run_time`, `query_max_memory`, `task_concurrency`, etc.) are set via `session_properties` in `profiles.yml` or `pre_hook` for one-off overrides. The plan declares non-default session properties.

## Article T6 — `on_table_exists` is an explicit choice

dbt-trino's table materialization supports two modes: `rename` (default) and `drop`. Plans for table-materialized models declare which mode applies, especially where the AWS Glue Metastore is the backend (Glue cannot rename — `drop` is required there).

## Article T7 — View security is declared

View materializations declare `view_security` as either `definer` (default — view runs as its creator) or `invoker` (runs as the caller). The default is fine for most cases; specs that require `invoker` semantics call this out explicitly because the downstream access pattern changes.

## Article T8 — Iceberg is the preferred destination format

When the destination catalog is configurable, models materialize into an Iceberg-backed catalog rather than Hive or external relational connectors. Reasons: Iceberg supports time travel, hidden partitioning, schema evolution, and works cleanly with dbt's incremental materializations. Plans that materialize into Hive or relational backends justify the choice (often: legacy constraint).

## Article T9 — Adapter is community-maintained

`dbt-trino` is maintained by Starburst, not by dbt Labs. Adapter-specific concerns (new features, breaking changes, version pinning) follow the dbt-trino release cadence, not dbt-core's. The `dependencies.yml` of any project using this preset pins `dbt-trino` to a known-good minor version range.

## Article T10 — Cost attribution is best-effort

Trino has no native query-tag-and-bill mechanism. Cost attribution depends on (a) session properties that include identifying tags, (b) log aggregation from coordinator-side query logs, and (c) connector-side billing for the underlying storage. Specs and plans note when cost attribution matters and how it will be achieved for this specific work.
```

### 8.12b `presets/trino/plan-additions.md`

```markdown
## Trino-specific concerns

### Catalogs and federation

| Catalog | Connector | Role in this work | Read / write |
|---|---|---|---|
| `iceberg` | Iceberg + S3 | destination for materialized models | read + write |
| `<source_catalog>` | <connector> | source data | read-only |

### Cross-catalog joins (Article T3)

| Model | Catalogs joined | Justification | Estimated rows moved over network |
|---|---|---|---|
| <model> | `<catalog_a>` × `<catalog_b>` | <why this join is necessary here and not earlier> | <estimate> |

If this table is empty, mark "none" — do not omit the table.

### Pushdown plan (Article T4)

| Model | Non-Iceberg sources | Predicates expected to push down | Verified via `EXPLAIN`? |
|---|---|---|---|
| <model> | `<catalog.schema.table>` | `<predicate_a>, <predicate_b>` | yes / no |

### Storage-format concerns

For each model materialized into an Iceberg-backed catalog:

| Model | Partitioning | File format | Compaction concerns |
|---|---|---|---|
| <model> | `<partition_spec>` (e.g., `day(event_ts)`) | parquet / orc | <how/when compaction runs> |

For non-Iceberg destinations, document the equivalent concerns for that table format.

### Session properties

| Property | Value | Justification |
|---|---|---|
| `query_max_run_time` | `<value>` | <why this differs from default> |
| `task_concurrency` | `<value>` | <why this differs from default> |

### Materialization choices

| Model | Materialization | `on_table_exists` | View security | Justification |
|---|---|---|---|---|
| <model> | table / view / incremental / materialized_view | rename / drop / n/a | definer / invoker / n/a | <why> |

### Cost attribution

| Risk | Mitigation |
|---|---|
| Cost of large cross-catalog scan invisible at review time | Add `EXPLAIN` output to the plan for any model with cross-catalog joins |
| Underlying connector (e.g., Hive on EMR) billed separately | Tag query via session property `application_name`; coordinator logs aggregated weekly |
```

### 8.12c `presets/trino/skills/trino-federated-query-patterns/SKILL.md`

```markdown
---
name: trino-federated-query-patterns
description: Use when designing a dbt-trino model that touches more than one Trino catalog, or when deciding whether a model should push work down to the underlying connector vs. pull into Trino.
---

# Federated query patterns on Trino

## When to use this skill

You're designing a model that touches more than one Trino catalog, OR you're trying to decide whether to make Trino compute something or push it back to the source. Both decisions are easy to get wrong by reflex and expensive to fix later.

## Mental model: Trino moves data, the connector stores it

Trino is a query engine. Storage lives in the underlying connectors:

- `iceberg` catalog → Parquet files in object storage, Iceberg table format
- `hive` catalog → files in object storage, Hive metastore
- `postgresql` catalog → an actual Postgres database
- `kafka` catalog → topic data via Kafka brokers
- `mongodb`, `elasticsearch`, etc. → analogous

The "warehouse" framing from Snowflake/Databricks doesn't apply. Every Trino model is a query plan that traverses these connectors and assembles results in Trino's memory. The question is always: *where is the work actually happening?*

## Decision 1: should this be a cross-catalog query at all?

**Prefer keeping the join inside one catalog when possible.** Cross-catalog joins:
- Move data over the network into Trino's coordinator/worker memory
- Defeat connector-side optimizations (Postgres index scans, Iceberg partition pruning of the other side)
- Make cost attribution harder

**Cross-catalog queries are fine when:**
1. The data really does live in different systems and no upstream pipeline can land it together
2. The non-Iceberg side is small (a dimension table, a config lookup)
3. You're in a lakehouse model that intentionally federates

**Cross-catalog queries are usually wrong when:**
1. The non-Iceberg side is large and you could `INSERT INTO iceberg.*.* SELECT FROM` it first
2. You're doing this "because Trino can" rather than because it's the best design
3. The same join pattern appears in 5+ marts (build a staged Iceberg table instead)

## Decision 2: pushdown — what work is the connector actually doing?

The cost difference between Trino-side filtering and connector-side filtering can be 1000x for large tables. The answer is in `EXPLAIN`.

### How to check pushdown

```sql
EXPLAIN (TYPE DISTRIBUTED)
SELECT count(*) FROM postgresql.public.orders WHERE created_at > date '2026-01-01';
```

In the output, look for:
- **`ScanFilterProject`** → filter is being applied by the connector (good)
- **`ScanProject` followed by `Filter` in a later stage** → connector returned all rows; Trino filtered after (bad)

### What typically pushes down

- Simple predicates on indexed columns (Postgres, MySQL): yes
- Predicates on partition columns (Iceberg, Hive): yes
- Aggregations on Iceberg with statistics: yes (Trino can sometimes answer `count(*)` from metadata)
- Joins to a small Trino-side table: usually does NOT push down (dynamic filtering helps)

### What typically does NOT push down

- Predicates on computed columns (`WHERE upper(name) = 'X'` against Postgres)
- Predicates involving Trino-specific functions
- Complex expressions involving multiple columns

## Decision 3: how to materialize for federation patterns

If a downstream model joins across catalogs frequently, **materialize the smaller side into Iceberg first.** This trades one batch write for many cheap reads.

```python
{{ config(
    materialized='table',
    catalog='iceberg',
    schema='cross_system',
    on_table_exists='rename'
) }}
SELECT customer_id, region, plan_tier
FROM postgresql.public.customer_profile
WHERE is_active = true
```

Then downstream marts join `iceberg.cross_system.customer_profile_cached` instead of the live Postgres source.

## Anti-patterns

- **Six-way join across six catalogs** — your plan is wrong; rebuild as a staged pipeline.
- **`WHERE source_data_lake.events.event_date > current_date - 7` without verifying pushdown** — silently scans the full table.
- **Materializing a Postgres-source model as a view** — every dashboard hit becomes a live Postgres query; usually wrong.
- **Joining a Kafka catalog to anything large** — Kafka connector reads sequentially; do not join to large catalogs.
- **Using `kafka.*.*` as a source without checking the connector's offset behavior** — re-reading topics in dbt is a foot-gun.

## In the spec/plan

The plan's "Cross-catalog joins" table makes every federation point visible. The "Pushdown plan" table makes every potentially-expensive predicate explicit. Reviewers verify `EXPLAIN` output is in the plan or attached.
```

### 8.13 `skills/writing-staging-model-specs/SKILL.md`

```markdown
---
name: writing-staging-model-specs
description: Use when writing the spec for a new dbt staging model (`stg_<source>__<entity>.sql`).
---

# Writing specs for dbt staging models

## When to use this skill

You're spec'ing a model in `models/staging/`. Staging models have a narrow, well-defined job — this skill keeps the spec tight.

## What a staging model does (and doesn't)

Staging models do:
- Rename columns to project conventions (snake_case, conventional suffixes like `_at`, `_id`)
- Cast types
- Filter out obvious junk (test rows, deletes, soft deletes)
- Generate surrogate keys via `dbt_utils.generate_surrogate_key`
- Apply masking for PII at the staging layer (never at the mart)

Staging models do NOT:
- Join across sources
- Compute business metrics
- Aggregate (one row in = one row out)
- Apply business logic that may change

## Template (additions to the base spec template)

```markdown
## Source

| Field | Value |
|---|---|
| Loader | <fivetran|airbyte|kafka|custom> |
| Source schema | `<raw_schema>` |
| Source table | `<table>` |
| Refresh cadence | <hourly|daily|...> |
| Loaded-at field | `<column>` |

## Column mapping

| Source column | Renamed to | Type cast | Notes |
|---|---|---|---|
| `id` | `<entity>_id` | `bigint` | natural key |
| `created_at` | `<entity>_created_at` | `timestamp_tz` | |
| `email` | `email_masked` | `string` | masked via policy `<name>` |

## Filter rules

- Drop rows where `<col> = '<test_marker>'`
- Drop rows where `is_deleted = true` (soft delete handling)
```

## Acceptance criteria patterns

Staging-flavored ACs that should always be present:

- AC: The system shall enforce uniqueness on `<entity>_id`.
- AC: The system shall enforce not-null on `<entity>_id` and `<entity>_created_at`.
- AC: When the source table receives a soft-deleted row, the system shall exclude it from the staging output.
- AC: Where PII columns exist, the system shall apply the masking policy `<name>`.

## Anti-patterns

- **Joining in staging** — push the join to intermediate or mart.
- **Computing metrics in staging** — push to mart.
- **Renaming in mart instead of staging** — rename once, at the staging boundary.
- **Skipping the loaded-at field declaration** — freshness tests break silently.
```

### 8.14 `skills/writing-mart-specs-with-grain/SKILL.md`

```markdown
---
name: writing-mart-specs-with-grain
description: Use when writing the spec for a dbt mart-layer model (`dim_*`, `fct_*`, or aggregated mart).
---

# Writing specs for dbt mart models — grain is everything

## When to use this skill

You're spec'ing a mart-layer model. The single most common failure mode for mart models is grain ambiguity — "what is one row in this table?" doesn't have a clean answer.

## The grain question must be answered first

Before anything else, the spec answers this in one sentence:

> One row in this table represents <one specific business event or entity>.

Examples:
- "One row represents one completed order at the time the order shipped."
- "One row represents one customer's state on a given day (daily snapshot)."
- "One row represents one session, where a session is defined as activity from one user with gaps no longer than 30 minutes."

If you can't answer in one sentence, the model needs to be split into two.

## Template (additions to the base spec template)

```markdown
## Grain

**One row represents:** <one specific business event or entity>

**Grain columns (unique key):** <col1, col2, col3>

**Type:** <event fact | snapshot fact | dimension (Type 1 / Type 2)>

## SCD strategy (dimensions only)

| Field | Type 1 (overwrite) | Type 2 (history) |
|---|---|---|
| `customer_name` | x | |
| `customer_tier` | | x |

## Late-arriving data handling

<How does the model handle records that arrive after the partition has already been processed? Reprocess window? Reject? Re-key?>

## Semantic layer alignment

| Metric / dimension | Provided by this model? | Notes |
|---|---|---|
| `total_revenue` | yes | sum of `order_amount` |
| `customer_tier` | yes (as a dim) | |
```

## Acceptance criteria patterns

- AC: The system shall enforce uniqueness on `<grain_cols>`.
- AC: When a source row arrives <N> days late, the system shall <reject | reprocess | append-only>.
- AC: Where this model feeds the semantic layer metric `<name>`, the system shall preserve the column `<col>` with stable name and type.

## Anti-patterns

- **Mart that combines multiple grains** — split into separate marts.
- **Grain that changes silently** — adding a new join key without spec change is a Constitution §11 violation.
- **No explicit late-arriving-data policy** — silent inconsistency follows.
- **Mart with `is_current` flag and no SCD strategy declared** — pick Type 2 with `valid_from`/`valid_to` instead.
```

### 8.15 `skills/writing-business-glossary-specs/SKILL.md` — THE WEDGE SKILL

```markdown
---
name: writing-business-glossary-specs
description: Use when writing a tier-3 spec that captures business domain context — entity definitions, grain decisions, cross-system identifier resolution.
---

# Writing business glossary specs

## When to use this skill

You're working on a data model where the *business meaning* of an entity isn't obvious from the source data. Examples:

- "Customer" means different things in Salesforce vs. Stripe vs. the product database.
- A "Well" is identified by EID across systems, but ProdView stores it as a Unit and ODA stores it as a Property — the grain is different and entity resolution is required.
- The marketing team's "session" and the product team's "session" have different boundaries.
- "Revenue" depends on whether you're talking GAAP-recognized, billed, or contracted.

This is the layer dbt-labs/dbt-agent-skills explicitly doesn't cover (see [dbt-core discussion #12521](https://github.com/dbt-labs/dbt-core/discussions/12521)) and where AI agents most often produce plausible-looking but business-wrong models.

## The three tiers (from the dbt-core discussion)

| Tier | Covers | Owner |
|---|---|---|
| 1 — Framework | "how to add a unit test", dbt mechanics | dbt-labs/dbt-agent-skills |
| 2 — Project | "our staging models use a 5-CTE pattern" | each project's CLAUDE.md |
| 3 — Business | "a Well is identified by EID across systems" | **this skill** |

## Template

```markdown
# Business glossary spec — <entity name>

## Definition

<One paragraph. What this entity IS in plain business language. Avoid technical jargon. If a non-technical stakeholder reads this, do they nod?>

## Canonical identifier

The canonical identifier for <entity> is `<column>`. All cross-system joins MUST resolve to this identifier.

## Source-system aliases

| System | Their name | Their identifier | Notes |
|---|---|---|---|
| Salesforce | `Account` | `Account.Id` (18-char) | also has 15-char `AccountId` — never use |
| Stripe | `Customer` | `Customer.id` | prefixed `cus_` |
| Internal product DB | `users.account_id` | `bigint` | |

## Entity resolution rules

<How do we resolve a record from System A to the canonical entity in System B? This is often non-trivial.>

1. Prefer match on `<external_id_field>` populated by the integration team.
2. Fall back to email-domain match for Salesforce ↔ product DB.
3. NEVER use name-similarity match.

## Grain decisions

When this entity appears in a model, the grain is one of:

- **point-in-time** (entity state as of timestamp T)
- **as-of-current** (latest known state)
- **event-sourced** (one row per change)

Specify which grain the model uses and why.

## Business rules

<The non-obvious rules a non-domain expert wouldn't know.>

- A customer with `is_test = true` is excluded from all financial reporting but included in product analytics.
- A customer is "active" if they had a billable event in the last 30 days, NOT if they have an active subscription record (legacy subscription records persist after churn).

## Common mistakes the AI agent must avoid

<Past errors that should not be repeated. This list grows over time.>

- Treating Salesforce's 15-char `Id` as canonical (it's not — the 18-char form is).
- Using `users.created_at` to compute customer tenure (use `accounts.signup_date` — `users.created_at` is the auth-system timestamp, not the customer's relationship start).
```

## Anti-patterns

- **Skipping this spec for "simple" entities** — even "user" has multiple definitions in most companies.
- **Writing the glossary spec inside the model spec** — the glossary outlives any single model; it's its own artifact.
- **Capturing business rules only in code comments** — they get lost in refactors.

## How to know this is working

Six months from now, a new analytics engineer joins the team and is asked to add a new mart that joins customer data across two source systems. They find this spec, follow the entity resolution rules, and produce a correct join on the first try without asking the original author. That's the bar.
```

### 8.16 `commands/dbt.specify.md`

```markdown
# /dbt.specify — draft a spec from a feature description

You are helping a dbt practitioner write a spec for a new feature or change.

## Read these first
1. `.dbt-specify/constitution.md` — the project's non-negotiable principles
2. `CLAUDE.md` — this project's conventions
3. `.dbt-specify/templates/spec-template.md` — the spec format

## What to do

Given the user's feature description:

1. Determine if this is a staging model, a mart, or something else. Load the relevant skill:
   - Staging: `.dbt-specify/skills/writing-staging-model-specs/SKILL.md`
   - Mart: `.dbt-specify/skills/writing-mart-specs-with-grain/SKILL.md`
   - Cross-system entity work: `.dbt-specify/skills/writing-business-glossary-specs/SKILL.md`

2. Generate the next spec number by listing `specs/` and incrementing the highest existing `<NNN>-` prefix.

3. Create `specs/<NNN>-<slug>/spec.md` from the template, filling in every section. Use information from the user's description; for anything not provided, ask one clarifying question per missing critical field. Maximum three clarifying questions total.

4. Write ACs in EARS format. Run `dbt-specify validate specs/<NNN>-<slug>/spec.md` to verify.

5. Tell the user the spec is ready for review and which file to open.

## Hard rules

- Do NOT write any code, models, tests, or YAML during this phase.
- Do NOT propose a plan during this phase.
- If the description is vague (e.g., "improve performance"), refuse and ask for specifics.
```

### 8.17 `commands/dbt.plan.md`

```markdown
# /dbt.plan — propose a plan from an approved spec

You are turning an approved spec into a file-by-file plan.

## Read these first
1. The current spec at `specs/<NNN>-<slug>/spec.md` (find the latest)
2. `.dbt-specify/constitution.md`
3. `.dbt-specify/templates/plan-template.md`
4. Existing repo structure: `models/`, `tests/`, `seeds/`, `macros/`, `_governance/`, `analyses/`

## What to do

1. Confirm the spec is marked **approved**. If not, refuse and tell the user to approve it first.

2. Generate `specs/<NNN>-<slug>/plan.md` from the template. For each section:
   - **Architecture** — 2–4 sentences referencing constitution articles
   - **Files to add/modify/delete** — exhaustive; one row per file
   - **Tests** — every AC must map to at least one test
   - **Risks** — at least two; one mitigated, one open
   - **Downstream impact** — search for exposures, semantic-layer references, reverse-ETL configs

3. The plan must respect the warehouse preset additions appended at the bottom of `plan-template.md`. Fill those tables in.

4. Open questions go in "Open questions for review" — do NOT silently make assumptions.

5. Mark the plan as **proposed** and tell the user to review and either approve or send back for revision.

## Hard rules

- Do NOT write any models or YAML during this phase.
- Do NOT skip the "Files to delete" section even if empty — write "(none)" if so.
- Every file in "Files to add" must trace to at least one AC.
```

### 8.18 `commands/dbt.tasks.md`

```markdown
# /dbt.tasks — decompose an approved plan into ordered tasks

You are turning an approved plan into a sequenced work breakdown.

## Read these first
1. The current plan at `specs/<NNN>-<slug>/plan.md`
2. `.dbt-specify/templates/tasks-template.md`

## What to do

1. Confirm the plan is marked **approved**. If not, refuse.

2. Generate `specs/<NNN>-<slug>/tasks.md` from the template.

3. Tasks are ordered by dependency:
   - sources.yml additions → staging models → intermediate → marts → exposures → grants → docs
   - Within each layer, alphabetical or by data flow

4. Each task has:
   - A unique id (T-01, T-02, ...)
   - An imperative one-line description
   - A "Done when" criterion that's observable
   - A "Validates" AC reference

5. Each task is small enough to commit as one logical change.

6. Tell the user the tasks are ready and they should approve before implementation.

## Hard rules

- Do NOT skip ahead to implementation in this phase.
- If a task feels larger than "one commit", split it.
- If a task can run in parallel with another, mark it `[P]` at the end of the description.
```

### 8.19 `commands/dbt.implement.md`

```markdown
# /dbt.implement — execute the next pending task

You are implementing one task from an approved tasks list.

## Read these first
1. The current `tasks.md`
2. The plan and spec it's derived from
3. `.dbt-specify/constitution.md`
4. The warehouse preset constitution additions (relevant to your warehouse)

## What to do

1. Find the next unchecked task in `specs/<NNN>-<slug>/tasks.md`.

2. Implement ONLY that task. Do not work ahead.

3. After implementation:
   - Run the validation step in the task's "Done when"
   - Run `dbt parse` to confirm the project still compiles
   - Run any relevant `dbt test` selectors
   - Check the task's box `[x]`
   - Stage and commit using the message format: `T-NN: <task description>` (commit body references the spec/plan paths)

4. Tell the user the task is complete and what's next.

## Hard rules

- Implement exactly one task per invocation.
- Do NOT add files not listed in the plan. If you discover a missing file, surface it to the user — do not create it silently.
- Do NOT modify files outside the plan's "Files to add/modify/delete" list. If you find a real bug elsewhere, write it to `specs/<NNN>-<slug>/findings.md` and continue.
- Do NOT mark the task complete if validation fails.
- Never auto-merge. Human approval is the final gate.
```

### 8.20 `examples/jaffle-shop-staging-overhaul/spec.md`

```markdown
# Jaffle Shop staging layer overhaul

**Ticket:** EX-001
**Author:** Example
**Date:** 2026-05-17
**Status:** approved

## Problem

The jaffle-shop staging models predate our current conventions. They don't follow the 5-CTE pattern, don't generate surrogate keys, and have inconsistent naming (some files use `stg__orders.sql`, others `stg_orders.sql`). New analytics engineers see them and either copy the wrong patterns or get confused about which is canonical.

## Users

| User | Job to be done |
|---|---|
| Analytics engineer joining the team | "I want to see one consistent staging pattern across all sources so I can ship my first model without guessing." |
| Senior analytics engineer reviewing PRs | "I want to stop manually pointing out the same staging-convention issues on every review." |

## What this is

Rewrite the jaffle-shop source's staging models (`stg_jaffle_shop__customers`, `stg_jaffle_shop__orders`, `stg_jaffle_shop__payments`) to follow the project's current 5-CTE pattern, with surrogate keys, explicit type casts, and consistent naming. No business-logic changes — same rows in, same rows out.

## Acceptance criteria

- AC1: The system shall produce three staging models named `stg_jaffle_shop__customers`, `stg_jaffle_shop__orders`, `stg_jaffle_shop__payments`.
- AC2: The system shall use the 5-CTE pattern (source → renamed → filtered → enhanced → final) in each staging model.
- AC3: The system shall generate a surrogate key column named `<entity>_sk` via `dbt_utils.generate_surrogate_key`.
- AC4: The system shall enforce `unique` and `not_null` on each surrogate key.
- AC5: When a downstream mart references the old staging model name, the system shall fail at parse time with a clear error.
- AC6: If a source row has `is_test = true`, then the system shall exclude it from the staging output.
- AC7: The system shall preserve the same row count (minus test rows) compared to the previous staging output, verified by a unit test fixture.

## Out of scope

- Adding new columns (we're refactoring, not extending)
- Modifying any intermediate or mart model
- Changing the jaffle-shop seed data
- Snowflake clustering (none of these tables exceed 1 GB)

## Constraints

- Warehouse: Snowflake
- Materialization: view (staging models stay as views)
- Grain: one row per source entity (orders/customers/payments), unchanged
- Refresh cadence: same as source (daily)
- Downstream consumers: `dim_customers`, `fct_orders`, `fct_payments` — all need to point at the new staging names

## Open questions

- [x] Drop the old `stg__orders.sql` (double underscore) immediately or keep as deprecated for one release? — **resolved: drop immediately, this is internal**
```

### 8.21 `examples/jaffle-shop-staging-overhaul/plan.md`

```markdown
# Plan — Jaffle Shop staging layer overhaul

**Spec:** ./spec.md
**Author:** AI agent (proposed) + senior eng (approved)
**Date:** 2026-05-17
**Status:** approved

## Architecture

Replace three legacy staging models with three new ones following the 5-CTE pattern (Constitution Articles §9, §10). Old files are deleted (not deprecated) per the resolved open question in the spec. Downstream marts are updated to reference the new model names; this is a coordinated change to maintain Constitution §11 ("no silent breaking changes").

## Files to add

| Path | Purpose |
|---|---|
| `models/staging/jaffle_shop/stg_jaffle_shop__customers.sql` | 5-CTE pattern, surrogate key |
| `models/staging/jaffle_shop/stg_jaffle_shop__orders.sql` | 5-CTE pattern, surrogate key |
| `models/staging/jaffle_shop/stg_jaffle_shop__payments.sql` | 5-CTE pattern, surrogate key |
| `models/staging/jaffle_shop/_jaffle_shop__sources.yml` | source declarations with freshness |
| `models/staging/jaffle_shop/_jaffle_shop__models.yml` | schema tests + docs |
| `tests/unit/test_stg_jaffle_shop__customers_excludes_test_rows.sql` | unit test for AC6 |
| `tests/unit/test_stg_jaffle_shop__orders_preserves_row_count.sql` | unit test for AC7 |

## Files to modify

| Path | Change |
|---|---|
| `models/marts/dim_customers.sql` | update `ref('stg__customers')` → `ref('stg_jaffle_shop__customers')` |
| `models/marts/fct_orders.sql` | update `ref('stg__orders')` → `ref('stg_jaffle_shop__orders')` |
| `models/marts/fct_payments.sql` | update `ref('stg__payments')` → `ref('stg_jaffle_shop__payments')` |
| `models/marts/_marts.yml` | no change needed; sk references go through the new staging models |

## Files to delete

| Path | Reason |
|---|---|
| `models/staging/jaffle_shop/stg__customers.sql` | replaced by new naming |
| `models/staging/jaffle_shop/stg__orders.sql` | replaced |
| `models/staging/jaffle_shop/stg__payments.sql` | replaced |

## Tests

| Test | AC covered |
|---|---|
| `unique` and `not_null` on `customer_sk`, `order_sk`, `payment_sk` | AC4 |
| Unit test: `stg_jaffle_shop__customers` excludes `is_test = true` rows | AC6 |
| Unit test: `stg_jaffle_shop__orders` row count = source row count - test row count | AC7 |
| `dbt parse` after delete of old models | AC5 |

## Risks

| Risk | Mitigation |
|---|---|
| Mart refs miss one of the old staging models, causing parse failure | Run `dbt parse` after each task; CI catches it in the worst case |
| Surrogate key generation introduces row mismatches if source columns are NULL | Unit test on row count (AC7) catches it; also `not_null` test catches it |
| Existing CI uses old staging names | Grep CI configs; updated in T-08 |

## Downstream impact

| Consumer | Impact | Notification |
|---|---|---|
| Semantic-layer metric `total_orders` | none (uses `fct_orders.order_id`, unchanged) | n/a |
| Exposure `weekly_revenue_dashboard` | none (downstream of `fct_orders`) | n/a |
| Reverse-ETL `hubspot_customer_sync` | additive: gains `customer_sk` column, no change to existing | confirmed with marketing-ops in Slack |

## Open questions for review

- [x] Drop old files immediately vs. deprecate? — resolved in spec
- [x] Snowflake clustering on these? — no, all <1 GB

<!-- BEGIN SNOWFLAKE PLAN ADDITIONS (auto-appended by dbt-specify) -->

## Snowflake-specific concerns

### Clustering decisions

| Model | Size estimate | Clustering key | Justification |
|---|---|---|---|
| stg_jaffle_shop__customers | <100 MB | none | small, view materialization, clustering N/A |
| stg_jaffle_shop__orders | <500 MB | none | below 1 GB threshold |
| stg_jaffle_shop__payments | <100 MB | none | below 1 GB threshold |

### Warehouse sizing

| Job | Warehouse | Size | Auto-suspend (s) | Justification |
|---|---|---|---|---|
| daily dbt build | `transform_wh` | X-Small | 60 | views only; no compute cost |

### Query tag plan

`project=jaffle_shop, model=stg_jaffle_shop__<entity>, env=<env>, run_id=<run_id>`

### Masking & governance

| Column | Source | Policy | Tested? |
|---|---|---|---|
| `email` | `raw.jaffle_shop.customers.email` | `mask_email` | yes (existing) |

### Cost guardrails

| Risk | Mitigation |
|---|---|
| view evaluation cost on dashboard hits | acceptable — views materialize on-read, downstream marts are tables |

<!-- END SNOWFLAKE PLAN ADDITIONS -->
```

### 8.22 `examples/jaffle-shop-staging-overhaul/tasks.md`

```markdown
# Tasks — Jaffle Shop staging layer overhaul

**Plan:** ./plan.md
**Status:** done

## Task list

- [x] **T-01** — Create `_jaffle_shop__sources.yml` with freshness and loaded-at fields for customers, orders, payments.
  - **Done when:** `dbt parse` succeeds and `dbt source freshness` runs against the sources.
  - **Validates:** AC1 (precondition)

- [x] **T-02** — Create `stg_jaffle_shop__customers.sql` using the 5-CTE pattern, with `customer_sk` via `dbt_utils.generate_surrogate_key`.
  - **Done when:** `dbt build --select stg_jaffle_shop__customers` runs green.
  - **Validates:** AC1, AC2, AC3

- [x] **T-03** — Create `stg_jaffle_shop__orders.sql` (same pattern).
  - **Done when:** `dbt build --select stg_jaffle_shop__orders` runs green.
  - **Validates:** AC1, AC2, AC3

- [x] **T-04** — Create `stg_jaffle_shop__payments.sql` (same pattern).
  - **Done when:** `dbt build --select stg_jaffle_shop__payments` runs green.
  - **Validates:** AC1, AC2, AC3

- [x] **T-05** — Create `_jaffle_shop__models.yml` with `unique` + `not_null` tests on each surrogate key.
  - **Done when:** `dbt test --select staging.jaffle_shop` runs green.
  - **Validates:** AC4

- [x] **T-06** — Create unit test `test_stg_jaffle_shop__customers_excludes_test_rows.sql`.
  - **Done when:** Test runs and fails when test-row filter is removed; passes when filter is present.
  - **Validates:** AC6

- [x] **T-07** — Create unit test `test_stg_jaffle_shop__orders_preserves_row_count.sql`.
  - **Done when:** Test passes against the fixture.
  - **Validates:** AC7

- [x] **T-08** — Update `dim_customers`, `fct_orders`, `fct_payments` mart refs to point at new staging model names.
  - **Done when:** `dbt parse` succeeds; `dbt build --select +dim_customers+ +fct_orders+ +fct_payments+` runs green.
  - **Validates:** AC5 (precondition — old refs would fail)

- [x] **T-09** — Delete `stg__customers.sql`, `stg__orders.sql`, `stg__payments.sql`.
  - **Done when:** `dbt parse` succeeds after deletion (proves AC5: no remaining ref to old names).
  - **Validates:** AC5

## Test plan

- [x] `dbt build --select +fct_orders+` runs green locally on a fresh schema
- [x] `dbt test` passes for all changed models
- [x] Unit tests for AC6 and AC7 are present and green
- [x] `weekly_revenue_dashboard` exposure still resolves

## Done definition

- [x] All tasks above are checked
- [x] All ACs are verified
- [x] Plan's downstream-impact actions completed (no external notifications needed for this refactor)
- [x] Retro filed (see `implementation-summary.md`)
```

### 8.23 `examples/jaffle-shop-staging-overhaul/implementation-summary.md`

```markdown
# Implementation summary — Jaffle Shop staging overhaul

**Date shipped:** 2026-05-17
**Lead time (spec to prod):** 4 hours

## Outcome

All seven ACs verified. Three legacy staging models replaced. Three marts updated. Old files deleted. CI green. No row-count regressions.

## What went well

- **Plan-first paid off.** The "Files to delete" table forced the agent to confront the downstream mart updates BEFORE writing code. In a vibe-coded version we would have deleted the old staging models first, broken the marts, then scrambled.
- **AC7 (row count preservation) caught a real bug.** The agent initially generated a surrogate key using `dbt_utils.generate_surrogate_key(['email'])` — but `email` is NULL for some test rows, so the surrogate key was non-deterministic. The row count test caught it; the fix was to include `customer_id` in the surrogate key inputs.

## What to change for next time

- **CLAUDE.md update:** Add an explicit rule that surrogate key inputs must include the natural primary key, never just business attributes. Filed as PR #<placeholder>.
- **New skill:** A `surrogate-key-generation` skill that captures this rule and the failure mode. Filed as PR #<placeholder>.

## Metrics

| Metric | Value |
|---|---|
| Plan-phase time | 25 minutes (mostly waiting for human review) |
| Implement-phase time | 1 hour 15 minutes |
| AI review findings | 2 (both fixed pre-merge) |
| Human review findings | 1 (the surrogate key issue caught by AC7) |
| Post-merge issues | 0 |

## Updates filed

- [x] CLAUDE.md change: PR #<placeholder>
- [x] New skill: PR #<placeholder>
- [x] Eval fixture for the surrogate-key edge case: PR #<placeholder>
```

---

## 9. Docs content

### 9.1 `docs/getting-started.md`

```markdown
# Getting started with dbt-spec-kit

Five-minute install + your first spec.

## Prerequisites

- Python 3.11+
- An existing dbt project (we don't generate dbt projects, we add spec-driven structure to them)
- An AI coding agent that reads markdown context (Claude Code, Cursor, GitHub Copilot, Gemini CLI, Cline, etc.)

## Install

The recommended path uses `uv` for isolated tool installation:

```bash
# install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# install dbt-specify as a tool
uv tool install dbt-spec-kit --from git+https://github.com/duckcode-ai/dbt-spec-kit.git
```

Verify:

```bash
dbt-specify --version
```

## Initialize in your dbt project

```bash
cd path/to/your-dbt-project
dbt-specify init my-project --warehouse snowflake
```

This creates:
- `.dbt-specify/constitution.md` — the project's non-negotiable principles
- `.dbt-specify/templates/` — spec, plan, tasks, retro
- `.dbt-specify/skills/` — tier-2 and tier-3 spec-writing skills
- `.dbt-specify/commands/` — slash-command prompts
- `CLAUDE.md` — the agent orientation file (or `CLAUDE.md.dbt-specify-suggested` if you already have one)
- `specs/` — empty directory for your first spec

## Compose with dbt-labs/dbt-agent-skills

Install dbt-agent-skills separately to cover the "how does dbt work" tier:

```bash
# Vercel Skills CLI path
npx skills add dbt-labs/dbt-agent-skills

# or via Tessl
tessl install dbt-labs/dbt-agent-skills
```

CLAUDE.md from `dbt-specify init` already defers tier-1 questions to that collection.

## Your first spec

In your AI agent, invoke `/dbt.specify <description of the feature>`. The agent will:

1. Read the constitution
2. Pick the right spec-writing skill (staging, mart, or business glossary)
3. Draft `specs/001-<slug>/spec.md`
4. Tell you to review

Once you approve, run `/dbt.plan` to get a plan, then `/dbt.tasks` to break it down, then `/dbt.implement` to execute one task at a time.

Validate your spec is EARS-conformant:

```bash
dbt-specify validate specs/001-<slug>/spec.md
```

## Next steps

- Read [methodology.md](methodology.md) for the full four-phase loop.
- Read [warehouse-guides/snowflake.md](warehouse-guides/snowflake.md) or [databricks.md](warehouse-guides/databricks.md) for your warehouse's preset.
- See [`examples/jaffle-shop-staging-overhaul/`](../examples/jaffle-shop-staging-overhaul/) for a complete worked example.
```

### 9.2 `docs/methodology.md`

```markdown
# Methodology — the four-phase loop, dbt-flavored

## Overview

```
Specify  →  Plan  →  Tasks  →  Implement
   ↑                                |
   └──────────  retro  ←────────────┘
```

Each phase has a **human checkpoint**. No phase skips, no auto-merge.

## Phase 1: Specify

**Input:** a feature description (one sentence or one paragraph).
**Output:** `specs/<NNN>-<slug>/spec.md`.
**Human checkpoint:** the spec is reviewed and marked `Status: approved`.

The spec answers: what problem, who's affected, what's the result, what are the acceptance criteria, what's out of scope, what are the constraints. ACs are EARS-formatted and validatable with `dbt-specify validate`.

If the spec describes a staging model, use the `writing-staging-model-specs` skill. For mart-level work, use `writing-mart-specs-with-grain`. For anything involving entities that span systems, also use `writing-business-glossary-specs`.

## Phase 2: Plan

**Input:** an approved spec.
**Output:** `specs/<NNN>-<slug>/plan.md`.
**Human checkpoint:** the plan is reviewed and marked `Status: approved`.

The plan enumerates every file that will be added, modified, or deleted; the tests for each AC; the warehouse-specific concerns (clustering, masking, governance, cost guardrails); and the downstream impact (semantic-layer metrics, exposures, reverse-ETL).

The warehouse preset's plan additions are appended automatically by `dbt-specify init`. Fill in the warehouse-specific tables before the plan is approved.

## Phase 3: Tasks

**Input:** an approved plan.
**Output:** `specs/<NNN>-<slug>/tasks.md`.
**Human checkpoint:** the tasks are reviewed and the engineer agrees the breakdown is right.

Tasks are ordered by dependency: sources → staging → intermediate → marts → exposures → grants → docs. Each task is small enough to be one logical commit. Each task lists its "Done when" criterion and the ACs it validates.

## Phase 4: Implement

**Input:** an approved tasks list.
**Output:** dbt project changes, one task at a time.
**Human checkpoint:** the engineer reviews and approves the final diff before merge.

`/dbt.implement` runs one task per invocation. After each task: validate, commit with the task-id message format, and stop. Never work ahead.

## The retro (not a separate phase, but mandatory)

After ship, the engineer (or agent under direction) writes a retro covering:
- What went well in the routine
- What to change for next time (CLAUDE.md updates, new skills, eval fixtures)
- Metrics: plan-phase time, implement-phase time, AI/human review findings, post-merge issues

Retros are filed as `specs/<NNN>-<slug>/retro.md` or appended to `implementation-summary.md`. CLAUDE.md and skills updates are filed as separate PRs so the methodology layer keeps improving.
```

### 9.3 `docs/ears-cheatsheet.md`

```markdown
# EARS cheatsheet — testable acceptance criteria for dbt specs

EARS = **Easy Approach to Requirements Syntax**. Five patterns. Every AC in every spec uses one.

## The five patterns

### 1. Ubiquitous — always true

> The system shall <response>.

Use for invariants. The thing is always required, no triggering condition.

**dbt examples:**
- The system shall produce a model named `dim_customers`.
- The system shall enforce `unique` and `not_null` on `customer_sk`.

### 2. Event-driven — triggered by an event

> When <trigger>, the system shall <response>.

Use for "when X happens, do Y."

**dbt examples:**
- When `dbt run` completes, the system shall write a `query_tag` to the audit table.
- When a source row arrives more than 7 days late, the system shall reject it.

### 3. State-driven — true while a state holds

> While <state>, the system shall <response>.

Use for ongoing conditions.

**dbt examples:**
- While the model is materialized as an incremental, the system shall use a `unique_key` of `<col>`.
- While the warehouse is paused, the system shall not trigger refreshes.

### 4. Unwanted condition — error handling

> If <unwanted>, then the system shall <response>.

Use for failure modes.

**dbt examples:**
- If a source row has `is_test = true`, then the system shall exclude it from the staging output.
- If `dbt parse` fails, then the system shall not deploy.

### 5. Optional — feature-flagged

> Where <feature>, the system shall <response>.

Use for behavior that's conditional on configuration.

**dbt examples:**
- Where Snowflake is the warehouse, the system shall apply the `mask_email` policy to PII columns.
- Where the semantic layer is enabled, the system shall preserve `<col>` with stable name and type.

## Anti-patterns

- "It should probably work" — not EARS. Not testable.
- "We want a fast model" — not EARS. Define "fast" as a measurable AC.
- "The user can do X" — not EARS. Reword as "When the user does Y, the system shall X."

## Validating

```bash
dbt-specify validate specs/<NNN>-<slug>/spec.md
```

Exits 0 if all AC lines match one of the five patterns. Exits 1 with a list of non-conformant lines otherwise.
```

### 9.4 `docs/warehouse-guides/snowflake.md`

```markdown
# Snowflake guide for dbt-spec-kit

## What `--warehouse snowflake` adds

`dbt-specify init --warehouse snowflake` appends Snowflake-specific articles to the constitution and Snowflake-specific tables to the plan template. These cover the concerns dbt-spec-kit's wedge is built around: warehouse-specific patterns dbt Labs intentionally doesn't ship.

## What's covered

| Topic | Where |
|---|---|
| Clustering keys | Constitution Article S1 + plan additions + clustering-decisions skill |
| Warehouse sizing | Constitution Article S2 + plan additions |
| Query tags | Constitution Article S3 + plan additions |
| Masking & row-access policies | Constitution Article S4 + plan additions |
| Dynamic tables | Constitution Article S5 |
| Cortex / LLM-powered transformations | Constitution Article S6 |

## Clustering — the most common question

Use the `snowflake-clustering-decisions` skill (installed at `.dbt-specify/skills/snowflake-clustering-decisions/SKILL.md`). The short version:

- Tables under 1 GB → no clustering
- Tables over 1 GB → cluster on the column most often in WHERE / JOIN
- Verify via `SYSTEM$CLUSTERING_INFORMATION` after first build

## Query tags — getting cost attribution right

Add to `dbt_project.yml`:

```yaml
on-run-start:
  - "{{ set_query_tag() }}"
```

Where `set_query_tag` is a macro that emits:

```jinja
{% macro set_query_tag() %}
    {% set tag %}
        project={{ project_name }}, model={{ this.name }}, env={{ target.name }}, run_id={{ invocation_id }}
    {% endset %}
    {% do run_query("ALTER SESSION SET QUERY_TAG = '" ~ tag ~ "'") %}
{% endmacro %}
```

Then attribute cost via:

```sql
SELECT query_tag, SUM(credits_used)
FROM snowflake.account_usage.query_history
GROUP BY 1;
```

## Masking — when staging is the right boundary

The constitution requires masking at the staging layer, not the mart. Reason: marts are often built from intermediate models that have already lost track of which columns are PII. Masking at staging keeps the boundary clean.

```yaml
# models/staging/<source>/_<source>__models.yml
- name: stg_<source>__customers
  columns:
    - name: email
      meta:
        masking_policy: mask_email
```

See `models/_governance/masking_policies.sql` for the policy definitions and `tests/unit/test_masking_policies.sql` for the deterministic-fixture tests.
```

### 9.5 `docs/warehouse-guides/databricks.md`

```markdown
# Databricks guide for dbt-spec-kit

## What `--warehouse databricks` adds

`dbt-specify init --warehouse databricks` appends Databricks-specific articles to the constitution and Databricks-specific tables to the plan template. The wedge is the same as for Snowflake: warehouse-specific patterns dbt Labs intentionally doesn't ship.

## What's covered

| Topic | Where |
|---|---|
| Liquid Clustering | Constitution Article D1 + plan additions + clustering-decisions skill |
| Photon | Constitution Article D2 + plan additions |
| Unity Catalog | Constitution Article D3 + plan additions |
| Materialized Views | Constitution Article D4 |
| Query tags via system tables | Constitution Article D5 |
| AI/ML governance (`ai_query`, Mosaic AI) | Constitution Article D6 |

## Liquid Clustering — the modern default

Liquid Clustering replaces rigid partitioning. Use the `databricks-liquid-clustering-decisions` skill for the decision rules. Short version:

- Use Liquid Clustering for tables >1 GB with selective query predicates
- One column is usually enough; up to 4 supported
- Compose with Predictive Optimization at the schema level

```sql
ALTER SCHEMA <catalog>.<schema> ENABLE PREDICTIVE OPTIMIZATION;
```

## Unity Catalog placement

All models use three-part names:

```sql
{{ config(
    materialized='table',
    catalog='analytics',
    schema='marts'
) }}
```

Grants live in `models/_governance/grants.sql` and apply as a post-hook:

```yaml
on-run-end:
  - "{{ apply_grants() }}"
```

## Materialized Views over hand-rolled incrementals

Where the warehouse supports it, prefer:

```python
{{ config(materialized='materialized_view') }}
```

Over:

```python
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='sync_all_columns'
) }}
```

The plan must justify any choice of `incremental` over `materialized_view`.

## Query tags via system tables

Databricks doesn't have inline `query_tag` like Snowflake. Use SQL warehouse tags + `system.access.audit`:

```sql
SELECT
  request_params:statement AS sql,
  request_params:warehouse_id AS warehouse,
  request_params:statement_id AS statement_id
FROM system.access.audit
WHERE service_name = 'databrickssql'
  AND date_trunc('day', event_time) = current_date();
```

Pair with workspace-level tags applied to the warehouse for full attribution.
```

### 9.6 `docs/warehouse-guides/trino.md`

```markdown
# Trino guide for dbt-spec-kit

## What `--warehouse trino` adds

`dbt-specify init --warehouse trino` appends Trino-specific articles to the constitution and Trino-specific tables to the plan template.

**Trino is not a warehouse.** It's a federated query engine. The constitution and plan additions reflect that — concerns center on catalogs, connectors, federation, pushdown, and session properties, not on warehouses or clustering.

## What's covered

| Topic | Where |
|---|---|
| Three-part naming (`catalog.schema.table`) | Constitution Article T2 + plan additions |
| Federation and cross-catalog joins | Constitution Article T3 + plan additions + federated-query-patterns skill |
| Connector pushdown | Constitution Article T4 + plan additions + skill |
| Session properties | Constitution Article T5 + plan additions |
| `on_table_exists: rename / drop` | Constitution Article T6 + plan additions |
| View security (`definer` / `invoker`) | Constitution Article T7 + plan additions |
| Iceberg as preferred destination | Constitution Article T8 |
| Adapter cadence (Starburst-maintained) | Constitution Article T9 |
| Cost attribution | Constitution Article T10 + plan additions |

## Three-part naming — the single most common Trino-on-dbt mistake

Always reference data with three parts:

```sql
SELECT * FROM iceberg.analytics.fct_orders;          -- right
SELECT * FROM postgresql.public.customers;           -- right
SELECT * FROM fct_orders;                            -- wrong: silent routing risk
```

The constitution enforces this. The plan template's catalog table makes every catalog touched visible.

## Federation — three good questions to ask before any cross-catalog join

1. **Should this join exist in Trino at all, or should one side be landed in Iceberg first?** Materializing the smaller side into Iceberg is often the right answer.
2. **What's the pushdown story?** Run `EXPLAIN (TYPE DISTRIBUTED)` and confirm the predicate appears in a `ScanFilterProject` node, not after the scan.
3. **What's the network cost?** Cross-catalog joins move data over the network. Estimate the rows pulled into Trino.

See `.dbt-specify/skills/trino-federated-query-patterns/SKILL.md` for the full decision rules.

## Session properties — replacing "warehouse sizing"

Trino doesn't have Snowflake's named warehouses. Adjust execution behavior via session properties:

```yaml
# profiles.yml
my_dbt_trino_project:
  target: prod
  outputs:
    prod:
      type: trino
      host: trino.example.com
      catalog: iceberg
      schema: analytics
      session_properties:
        query_max_run_time: '30m'
        query_max_memory: '4GB'
        task_concurrency: 8
```

Per-model overrides via `pre_hook`:

```python
{{ config(
    materialized='table',
    pre_hook=["set session query_max_run_time='10m'"]
) }}
```

## `on_table_exists` — choose deliberately, especially on Glue

```python
{{ config(
    materialized='table',
    on_table_exists='rename'   -- default; safer
) }}
```

But if your underlying metastore is AWS Glue and the target catalog is Hive-style:

```python
{{ config(
    materialized='table',
    on_table_exists='drop'     -- required; Glue cannot rename
) }}
```

Constitution Article T6 makes this an explicit choice in the plan, not a default-and-hope.

## View security

```python
{{ config(
    materialized='view',
    view_security='definer'    -- default; view runs as creator
) }}
```

Use `'invoker'` only when downstream users must be enforced against their own access controls. The plan declares the choice.

## Cost attribution (best-effort)

Trino has no native cost-tag mechanism. The viable patterns:

1. Set `application_name` or a custom session property at run time so queries are identifiable in coordinator logs.
2. Aggregate from coordinator query logs into an Iceberg table for analysis.
3. Attribute storage cost separately via the underlying connector's billing (Iceberg/S3 lifecycle policies).

The plan's "Cost attribution" table makes the chosen approach explicit.

## Composition with the lakehouse pattern

The most common Trino-on-dbt deployment is the **lakehouse pattern**: Iceberg tables in S3 (or equivalent object store), Trino as the query engine, dbt as the transformation layer. The constitution and plan additions assume this pattern as default but do not require it — non-Iceberg catalogs are supported with explicit annotation.
```

---

## 10. Hand-off prompt for Claude Code

When you're ready, point Claude Code at this repo with one prompt. Something like:

> I'm handing you a fully-specified open-source project to build from scratch. Read `PLAN.md` end-to-end before doing anything. It contains the constitution, spec, plan, ordered task list (sections 5), and full content for every file (sections 6–9). Implement tasks in order. After each task, run its validation step. Commit with the format `T-NN: <imperative summary>`. If you have questions the plan doesn't answer, append them to `QUESTIONS.md` and pick the answer that best aligns with the Mission (section 1) and Constitution (section 2). Do not add features not in this plan — surface them to `FOLLOWUP.md` instead.

That's it.

---

## 11. After v0.1 — explicit follow-up backlog

Do not build these in v0.1. They are listed here so the plan is honest about scope.

- **BigQuery preset** (v0.2) — `presets/bigquery/` with partitioning, clustering, BI Engine, materialized-view considerations
- **Redshift preset** (v0.3) — `presets/redshift/` with sort keys, dist keys, RA3 vs. RA4 sizing, late-binding views
- **Iceberg-engine preset** (v0.4+) — `presets/iceberg-engine/` for stacks where the "warehouse" is an Iceberg query engine (DuckDB-Wasm, Tabular-style deployments, federated lakehouses) rather than a managed warehouse
- **`dbt deps` skills integration** — when [dbt-core issue #12868](https://github.com/dbt-labs/dbt-core/issues/12868) ships, add `dependencies.yml` support so dbt-spec-kit can be installed via `dbt deps`
- **Slash-command preset** — when an agent supports Spec Kit's preset/extension mechanism, ship a preset so users can `specify preset add dbt-spec-kit` from upstream spec-kit
- **A VS Code extension** — only if user demand justifies it; spec-kit itself is also exploring this
- **More tier-3 skills** — sessions, revenue (GAAP vs. billed vs. contracted), churn-vs-attrition, entity-resolution playbooks for common SaaS source systems
- **An asciinema demo embedded in the README**
- **A `dbt-specify migrate-from-claude-md` command** that reads an existing CLAUDE.md and proposes a spec-kit-style structure
- **A `dbt-specify retro` command** that generates a retro template from the spec/plan/tasks state of a feature directory

— end of plan —
