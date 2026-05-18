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
- [ ] `dbt-specify validate project` passes
- [ ] `dbt-specify validate dbt --manifest target/manifest.json` passes after `dbt parse`
- [ ] Unit tests for AC3 and AC4 are present
- [ ] Downstream exposures still resolve

## Done definition

<The whole feature is done when:>

- [ ] All tasks above are checked
- [ ] All ACs are verified
- [ ] Plan's downstream-impact actions have been completed
- [ ] Retro is filed (see retro-template.md)
