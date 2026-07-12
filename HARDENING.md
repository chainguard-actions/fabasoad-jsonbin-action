<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v3.0.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **fabasoad--jsonbin-action/v3.0.1** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference actions/reusable workflows by mutable tag or branch instead of a pinned full-length SHA commit hash. This exposes the workflow to supply-chain attacks if the referenced ref is updated maliciously.

- functional-tests.yml: `uses: actions/checkout@v7` (tag, not SHA)
- linting.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-pre-commit.yml@main` (branch, not SHA)
- release.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-github-release.yml@main` (branch, not SHA)
- security.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-security-sast.yml@main` (branch, not SHA)
- sync-labels.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-sync-labels.yml@main` (branch, not SHA)
- update-license.yml: `uses: fabasoad/reusable-workflows/.github/workflows/wf-update-license.yml@main` (branch, not SHA)

Locations:

- `.github/workflows/functional-tests.yml:42`
- `.github/workflows/linting.yml:12`
- `.github/workflows/release.yml:11`
- `.github/workflows/security.yml:14`
- `.github/workflows/sync-labels.yml:10`
- `.github/workflows/update-license.yml:10`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned all 6 unpinned action references to full SHA commit hashes:
- functional-tests.yml: actions/checkout@v7 → @9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
- linting.yml: fabasoad/reusable-workflows/.github/workflows/wf-pre-commit.yml@main → @e4ff663d3bc9ff9d225d2e967a0f94aad342d218 # main
- release.yml: fabasoad/reusable-workflows/.github/workflows/wf-github-release.yml@main → @e4ff663d3bc9ff9d225d2e967a0f94aad342d218 # main
- security.yml: fabasoad/reusable-workflows/.github/workflows/wf-security-sast.yml@main → @e4ff663d3bc9ff9d225d2e967a0f94aad342d218 # main
- sync-labels.yml: fabasoad/reusable-workflows/.github/workflows/wf-sync-labels.yml@main → @e4ff663d3bc9ff9d225d2e967a0f94aad342d218 # main
- update-license.yml: fabasoad/reusable-workflows/.github/workflows/wf-update-license.yml@main → @e4ff663d3bc9ff9d225d2e967a0f94aad342d218 # main

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Prepare GET headers' step of .github/workflows/functional-tests.yml. Moved ${{ secrets.JSONBIN_MASTER_KEY }} and ${{ secrets.JSONBIN_ACCESS_KEY }} from direct interpolation in the run: shell command (--arg mk '${{ secrets.JSONBIN_MASTER_KEY }}' and --arg ak '${{ secrets.JSONBIN_ACCESS_KEY }}') into an env: block as MK and AK respectively. The shell script now references them as "$MK" and "$AK" environment variables.

