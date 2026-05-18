# Releasing to PyPI

dbt-spec-kit publishes to PyPI through PyPI Trusted Publishing. The release workflow does not use a
PyPI password or API token. GitHub Actions requests a short-lived OIDC token, PyPI verifies the
repository, workflow, and environment claims, and then accepts the package upload.

## One-time setup

Configure these two systems before publishing the first release.

### PyPI

Create a pending Trusted Publisher for the package:

- PyPI project name: `dbt-spec-kit`
- Owner: `duckcode-ai`
- Repository name: `dbt-spec-kit`
- Workflow name: `release.yml`
- Environment name: `pypi`

Pending publishers can create the PyPI project on first publish, but they do not reserve the name
before that first successful upload.

### GitHub

In the GitHub repository, create an environment named `pypi`.

Recommended controls:

- Require reviewer approval for deployments to the environment.
- Limit who can approve the environment to the package maintainers.
- Restrict deployments to protected release refs when the repository policy supports it.

The workflow file must live at `.github/workflows/release.yml`, because PyPI checks the workflow
filename against the Trusted Publisher configuration.

## Release process

1. Update `pyproject.toml` to the release version.
2. Move the relevant `CHANGELOG.md` notes from `Unreleased` into the release section.
3. Merge the release PR to `main`.
4. Create and push a tag that exactly matches the package version, prefixed with `v`.

```bash
git checkout main
git pull --ff-only origin main
git tag v1.0.0
git push origin v1.0.0
```

5. Create a GitHub Release from that tag and publish it.
6. Approve the `pypi` environment deployment if GitHub asks for approval.
7. Confirm the package is visible at <https://pypi.org/project/dbt-spec-kit/>.

The release workflow verifies that the GitHub Release tag matches the `pyproject.toml` version. A
release tagged `v1.0.0` must publish package version `1.0.0`; mismatches fail before upload.

## Install from PyPI

Users can install from PyPI:

```bash
uvx --from dbt-spec-kit dbt-specify --version
uvx --from dbt-spec-kit dbt-specify init my-project --warehouse snowflake
```

Persistent install:

```bash
uv tool install dbt-spec-kit
dbt-specify --version
```

`pipx install dbt-spec-kit` also works for teams that do not use `uv`.

## If publishing fails

- `invalid-publisher`: Check the PyPI Trusted Publisher values exactly match `duckcode-ai`,
  `dbt-spec-kit`, `release.yml`, and `pypi`.
- `tag mismatch`: Update `pyproject.toml` or create the correct `vX.Y.Z` tag.
- `file already exists`: PyPI does not allow replacing an existing version. Bump the version and
  publish a new release.
- `environment approval pending`: Approve the `pypi` deployment in GitHub Actions.
