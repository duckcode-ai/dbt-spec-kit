# Follow-up

Ideas, gaps, and scope-creep observations that were noticed during the v0.1 build but
intentionally not acted on. Each entry should include: what was noticed, where, and a
recommendation. Triaged by the maintainer after v0.1 ships.

## Found during build

- **Task: T-07 (Phase A) — `templates_loader.py` editable-install path.** PLAN Section 6.6 reads assets via `importlib.resources.files("dbt_specify") / "_assets" / kind`. In a `pip install -e .` editable install, the `_assets/` tree never gets created — hatch's `force-include` only applies at wheel build time. Recommendation: keep the current resolver (it falls back to top-level `<kind>/` dirs when the packaged path is missing), or restructure assets to live inside `src/dbt_specify/_assets/` directly. Did not change the source layout because PLAN Section 4.1 pins the directory tree.
- **Task: T-07 (Phase A) — `templates_loader.py` ruff `UP033`.** PLAN Section 6.6 uses `@lru_cache(maxsize=None)` which ruff `UP033` flags as superseded by `@functools.cache` on Python 3.9+. Switched to `@cache`; semantics are identical. Surfacing here because PLAN says "copy verbatim unless you spot a bug."
