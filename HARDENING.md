<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v3.0.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v3.0.1** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: The 'Prepare GET headers' step in functional-tests.yml directly interpolates `${{ secrets.JSONBIN_MASTER_KEY }}` and `${{ secrets.JSONBIN_ACCESS_KEY }}` inside a `run:` shell block (lines 35–36). Any `${{ ... }}` expression interpolated directly into a `run:` script is a script-injection finding because the YAML template engine substitutes the value before the shell ever sees it, bypassing shell quoting. These values should be passed via `env:` variables and referenced as `$ENV_VAR` inside the script instead.

Locations:

- `.github/workflows/functional-tests.yml:35`
- `.github/workflows/functional-tests.yml:36`

### unpinned-uses (severity: high)

Multiple workflow files reference actions or reusable workflows using mutable tags or branch names instead of immutable full 40-character SHA digests, making them vulnerable to supply-chain attacks:
- functional-tests.yml: `uses: actions/checkout@v7` (version tag, not a SHA)
- linting.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-pre-commit.yml@main` (branch)
- release.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-github-release.yml@main` (branch)
- security.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-security-sast.yml@main` (branch)
- sync-labels.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-sync-labels.yml@main` (branch)
- update-license.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-update-license.yml@main` (branch)
All of these should be pinned to a full commit SHA (e.g. `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4`).

Locations:

- `.github/workflows/functional-tests.yml:42`
- `.github/workflows/linting.yml:13`
- `.github/workflows/release.yml:12`
- `.github/workflows/security.yml:17`
- `.github/workflows/sync-labels.yml:11`
- `.github/workflows/update-license.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses

**Notes:**

Fixed script-injection in functional-tests.yml by moving JSONBIN_MASTER_KEY and JSONBIN_ACCESS_KEY secrets from inline ${{ }} interpolation in the run: block into the step's env: block, referencing them as plain shell variables. Pinned all 6 unpinned action/workflow references to full 40-character commit SHAs: actions/checkout@v7 → @3d3c42e5aac5ba805825da76410c181273ba90b1 # v7, and all 5 fabasoad/reusable-workflows @main references → @c5bd8945762dab6d2f5168b65f10355887ea40a3 # main across linting.yml, release.yml, security.yml, sync-labels.yml, and update-license.yml.

