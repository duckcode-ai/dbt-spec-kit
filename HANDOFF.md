# Hand-off to Claude Code — dbt-spec-kit v0.1 build

**Read this entire file before doing anything else.** It tells you how to operate inside this specific repo for this specific build. After you read this, read `PLAN.md` end-to-end. Then start work.

---

## TL;DR

You are autonomously building `dbt-spec-kit` v0.1 in **the existing GitHub repo `duckcode-ai/dbt-spec-kit`**. The full project specification is in `PLAN.md` in this directory. PLAN.md contains the constitution, spec, plan, ordered task list (50 tasks across 9 phases), and full content for every file (sections 6–9 of PLAN.md).

Your job: implement every task in order, **one PR per phase** (9 PRs total, A through I), push branches to `origin`, open PRs against `main`. **You will auto-merge each PR once CI passes** (`gh pr merge --auto --squash`). The human operator is NOT in the loop on merges — they observe, intervene only if something looks wrong.

---

## 1. Repo coordinates and starting state

- **Repo:** `https://github.com/duckcode-ai/dbt-spec-kit`
- **Default branch:** `main`
- **Your remote name:** `origin`

**Before doing anything, run the inventory step:**

```bash
git remote -v
git status
ls -la
git log --oneline -10 2>/dev/null || echo "no commits yet"
```

You will see one of three states:

**State 1 — Empty repo (most likely).** No files except possibly `.git/`, `README.md`, `LICENSE`, or `.gitignore`. Treat this as a greenfield build. Proceed with the full PLAN.md as written.

**State 2 — Partial scaffolding.** Some files exist already (maybe a README, a LICENSE, a `.gitignore`, or even an early `pyproject.toml`). Do NOT clobber them. Instead:
1. Read what's there.
2. If `LICENSE` exists and is MIT, keep it. If it's anything else, write to `LICENSE-PROPOSED.md` and surface to the operator in your first PR description.
3. If `README.md` exists with real content, write your README from PLAN.md Section 7.1 to `README-NEW.md`, leave the original in place, and surface in the PR.
4. If `pyproject.toml` exists, read it carefully and adapt — do not overwrite blindly.
5. If a fully-formed dbt-spec-kit already exists (e.g., the operator started a build elsewhere), STOP and write your observations to `OBSERVATIONS.md`, then ask for guidance.

**State 3 — Repo has commit history unrelated to dbt-spec-kit.** Same rules as State 2 — never destroy existing work without explicit instruction.

---

## 2. Branching and PR strategy — one PR per phase

PLAN.md Section 5 organizes the 50 tasks into 9 phases (A–I). You will open one PR per phase. Total: 9 PRs.

| Phase | Tasks | Branch name | PR title |
|---|---|---|---|
| A | T-01 to T-08 | `phase-a-foundation` | `Phase A: foundation — pyproject, CLI skeleton, constitution, templates` |
| B | T-09 to T-14a | `phase-b-init-command` | `Phase B: init command — implement and test against three warehouses` |
| C | T-15 to T-23 | `phase-c-warehouse-presets` | `Phase C: warehouse presets — Snowflake, Databricks, Trino` |
| D | T-24 to T-26 | `phase-d-skills` | `Phase D: tier-2 and tier-3 skills` |
| E | T-27 to T-30 | `phase-e-slash-commands` | `Phase E: slash-command prompts` |
| F | T-31 to T-34 | `phase-f-validate-command` | `Phase F: validate command — EARS validator and tests` |
| G | T-35 to T-38 | `phase-g-worked-example` | `Phase G: worked example — jaffle-shop staging overhaul` |
| H | T-39 to T-46 | `phase-h-docs-and-ci` | `Phase H: docs, CI workflow, README/CHANGELOG/CONTRIBUTING` |
| I | T-47 to T-50 | `phase-i-final-polish` | `Phase I: final polish — full test pass, version tag` |

### Workflow per phase

For every phase, in order, do exactly this:

```bash
# 1. Make sure local main is up to date
git checkout main
git pull origin main

# 2. Create the phase branch from main
git checkout -b phase-<letter>-<slug>

# 3. Implement every task in the phase, in order.
#    After EACH task within the phase:
#      - run the task's validation step (from PLAN.md Section 5)
#      - if validation passes, commit using:
#        git add -A
#        git commit -m "T-NN: <imperative summary>"
#      - if validation fails, debug until green; never commit a red task

# 4. After ALL tasks in the phase are committed, push the branch
git push -u origin phase-<letter>-<slug>

# 5. Open a PR against main using gh
gh pr create \
  --base main \
  --head phase-<letter>-<slug> \
  --title "Phase <letter>: <phase summary>" \
  --body "$(cat <<'EOF'
## Summary

<one-sentence summary of what this phase delivers>

## Tasks completed (from PLAN.md Section 5)

- T-NN — <one-line description>
- T-NN — <one-line description>
- ...

## Acceptance criteria addressed (from PLAN.md Section 3.3)

- AC<N>: <one-line how this phase contributes>

## Validation

- [ ] All task-level validation steps green locally
- [ ] CI green (lint, mypy, pytest) — applies once Phase A lands the CI workflow
- [ ] No unrelated changes outside the phase scope

## Build notes

<anything notable: surprises, decisions made under ambiguity, items written to FOLLOWUP.md or QUESTIONS.md. The human operator can read these post-merge to triage anything that needs follow-up.>
EOF
)"

# 6. Enable auto-merge on the PR.
#    Phase A is special — see below.
#    For Phase B onward:
gh pr merge --auto --squash --delete-branch

# 7. WAIT for the PR to merge. Auto-merge fires once all required checks pass.
#    Poll every ~2 minutes: gh pr view <pr-number> --json state,mergedAt
#    Do NOT start the next phase until you see state=MERGED.
#    Once merged, pull main locally and proceed to the next phase.

git checkout main
git pull origin main
```

### Phase A — special handling

Phase A is special because it *lands* the CI workflow itself. Until Phase A merges, no CI exists on the repo, so `gh pr merge --auto` has nothing to wait for.

For Phase A only:

1. Before pushing, run the full validation locally yourself:
   ```bash
   ruff check src tests
   mypy src
   pytest -v
   ```
2. Only push the branch and open the PR if all three are green locally.
3. Use `gh pr merge --squash --delete-branch` (no `--auto`) to merge immediately after opening the PR. This is the one phase where you merge directly because there's no CI to wait for.
4. Pull main and continue to Phase B normally.

From Phase B onward, CI exists, `--auto` works, and you wait for the green-CI merge signal before proceeding.

### Hard rules for the git workflow

- **Never push directly to `main`.** Every change goes through a phase branch and a PR. Even with auto-merge, the PR is the audit trail.
- **Auto-merge only fires when CI is green.** Do NOT use `--admin` or any flag that bypasses required checks. If CI fails, fix it on the branch; do not force a merge.
- **Phase A merges without `--auto`** because the CI workflow it ships doesn't exist on main yet. See "Phase A — special handling" above.
- **Never force-push** an open PR branch unless explicitly told. If you need to rewrite history, surface it first.
- **Never branch off another phase branch.** Always branch off `main` after the previous phase has merged.
- **If `main` advances during a phase** (operator pushed a hotfix, for example), rebase your phase branch onto the new `main` before opening the PR: `git rebase origin/main`. If rebase has conflicts, surface them — do not force-resolve.
- **Commit messages follow the format `T-NN: <imperative summary>`** — one commit per task. Multi-task commits are forbidden in this build. (Yes, that means ~50 commits across 9 PRs. That's intentional — it matches the spec-kit dogfooding story PLAN.md is selling. The squash-merge in step 6 collapses these into one commit per phase on `main`, but the PR-level history preserves the per-task trail.)

---

## 3. What to do when things go wrong

### CI fails on an open PR

1. Do not start the next phase.
2. Read the CI logs via `gh run view --log-failed` or `gh pr checks`.
3. Fix the issue in a new commit on the same phase branch. Commit message: `T-NN-fix: <what you changed>` (or `phase-<letter>-fix: ...` for cross-task fixes).
4. Push; CI re-runs.
5. Wait for green.

### You find a real bug or gap in PLAN.md

1. Do NOT silently fix it in code.
2. Append an entry to `FOLLOWUP.md` (in the repo root) under a `## Found during build` heading.
3. Include: which task you were on, what you noticed, what you'd recommend, why you didn't act on it now.
4. Continue with what PLAN.md says.

### You have a question PLAN.md doesn't answer

1. Re-read PLAN.md Section 1 (Mission) and Section 2 (Constitution). The answer is often there indirectly.
2. If still unclear, append to `QUESTIONS.md` (in the repo root) with: the task, the question, the answer you chose, and why.
3. Pick the answer that best aligns with Mission and Constitution. Continue.

### Auto-merge isn't firing (CI stuck or required check missing)

Polling cadence: check every 2 minutes with `gh pr view <pr-number> --json state,statusCheckRollup`. Possible states and what to do:

- **CI still running** — wait. CI typically finishes in <5 minutes per phase. If it's been >15 minutes, check `gh run list --branch <branch>` to see if anything is queued or stuck.
- **CI failed** — read the failed step with `gh run view --log-failed`. Fix on the branch with a `T-NN-fix:` or `phase-<letter>-fix:` commit. Push. Wait for re-run.
- **CI is green but auto-merge didn't fire** — check branch protection rules with `gh api repos/duckcode-ai/dbt-spec-kit/branches/main/protection`. If a required check isn't reporting, run `gh pr merge --squash --delete-branch` manually (no `--auto`).
- **PR has merge conflicts with `main`** — rebase onto latest main: `git fetch origin main && git rebase origin/main`. Resolve only conflicts that belong to your branch; if you see unfamiliar code, stop and write to `WAITING.md`.
- **30 minutes have passed with no progress** — stop, write a summary to `WAITING.md`, and stop polling. Do not start the next phase.

### You realize a previous phase has a bug

1. Do NOT fix it on the current phase branch — that mixes scope.
2. Write the bug to `FOLLOWUP.md` with severity (blocker / non-blocker).
3. If it's a blocker for the current phase, stop, open a separate hotfix PR off `main` with branch `hotfix-<short-name>`, fix only that one issue, auto-merge that PR (`gh pr merge --auto --squash --delete-branch`), wait for the merge, then rebase the current phase branch onto the new main before continuing.
4. If non-blocker, continue current phase; the operator will triage FOLLOWUP.md after the build.

---

## 4. What stays out of git

These files exist as build artifacts and should be kept out of the repo:

- `WAITING.md` (if created — local-only, gitignored)
- Any local `.venv/` (already in `.gitignore` from Phase A)
- `.dbt-specify/` directories inside `tests/fixtures/` AFTER tests run — these are test outputs

`PLAN.md`, `HANDOFF.md` (this file), `FOLLOWUP.md`, `QUESTIONS.md`, and `CHANGELOG.md` ALL stay in the repo. They are the dogfooding evidence.

Actually — one exception. **`HANDOFF.md` (this file) is removed in Phase I**, since it's operationally specific to the v0.1 build and isn't useful to repo visitors after the fact. Task T-50 deletes it as the last step before the version tag. PLAN.md stays.

---

## 5. Pre-flight checklist — run these once before Phase A

```bash
# 1. Confirm gh is authenticated to the right account
gh auth status

# 2. Confirm you can talk to the repo
gh repo view duckcode-ai/dbt-spec-kit

# 3. Confirm Python 3.11+ is available
python --version

# 4. Confirm uv is available (used for testing the install path in T-50)
uv --version || echo "uv not installed — install before Phase I"

# 5. Confirm git identity is set sensibly
git config user.name
git config user.email
# If these are empty or wrong for the duckcode-ai context, set them:
# git config user.name "Claude Code"
# git config user.email "claude-code@anthropic.com"
# (Or whatever values the operator prefers — but they should be obvious-not-personal.)

# 6. Check branch protection settings on `main` — auto-merge requires the right config
gh api repos/duckcode-ai/dbt-spec-kit/branches/main/protection 2>/dev/null || echo "no protection configured"
```

### Required branch-protection state for auto-merge

For the auto-merge workflow to function:

- **Required status checks**: at least one (the CI workflow `ci` from Phase A). Without this, `--auto` has nothing to wait for and PRs sit forever.
- **Required approvals**: **0**. If approvals are required, `--auto` can never fire (you are the only person on the repo).
- **Allow auto-merge**: must be enabled at the repo level.
- **Restrict who can push to matching branches**: optional but recommended (limit to repo admins only).

If branch protection is not yet configured, surface this to the operator BEFORE Phase A. The operator can configure it via Settings → Branches → Add rule, or via `gh`:

```bash
# After Phase A merges (so the ci workflow exists), set protection:
gh api repos/duckcode-ai/dbt-spec-kit/branches/main/protection \
  --method PUT \
  --raw-field 'required_status_checks={"strict":true,"contexts":["ci"]}' \
  --field 'required_pull_request_reviews=null' \
  --field 'enforce_admins=false' \
  --field 'restrictions=null'

gh api repos/duckcode-ai/dbt-spec-kit \
  --method PATCH \
  --field allow_auto_merge=true \
  --field delete_branch_on_merge=true
```

**Note**: branch protection cannot be set before the `ci` workflow exists on main, because GitHub validates that the required-check name exists. So the actual sequence is:
1. Phase A ships (no protection yet, direct merge as described above).
2. Configure branch protection (above commands).
3. Phase B onward uses `--auto` against the configured protection.

If any pre-flight step fails, surface it to the operator and wait.

---

## 6. The hand-off prompt (this is what the operator already gave you)

> Read HANDOFF.md first, then PLAN.md end-to-end. You are autonomously building `dbt-spec-kit` v0.1 in the GitHub repo `duckcode-ai/dbt-spec-kit`. Implement 50 tasks across 9 phases. One PR per phase. Never push to main directly. Use `gh pr merge --auto --squash --delete-branch` to auto-merge each PR once CI passes (Phase A is special — see HANDOFF.md). Wait for each PR to merge before starting the next phase. Commit messages follow `T-NN: <imperative summary>`. If you have questions, append to QUESTIONS.md and pick the answer that best fits Mission (Section 1) and Constitution (Section 2). If you spot bugs or scope creep ideas, append to FOLLOWUP.md and do not act on them.

---

## 7. Definition of "done" for the whole build

The entire v0.1 build is done when:

1. All 9 phase PRs are merged to `main`.
2. The repo has the directory tree described in PLAN.md Section 4.1.
3. CI is green on `main`.
4. The tag `v0.1.0` has been created and pushed.
5. `uvx --from git+https://github.com/duckcode-ai/dbt-spec-kit.git dbt-specify init test-project --warehouse trino` works end-to-end against a minimal dbt project fixture.
6. `HANDOFF.md` has been removed from `main` (task T-50).
7. PLAN.md is still present at the repo root as the dogfooding artifact.

When you reach this state, your final action is to write a summary of the build to `BUILD-SUMMARY.md` (in the repo root, committed via a final small PR `build-summary` with auto-merge). The summary should include: total commits, total PRs, any QUESTIONS.md entries, any FOLLOWUP.md entries, and the duration of the build. Then stop.

---

— end of hand-off —
