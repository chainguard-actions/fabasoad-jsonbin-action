<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.6

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v2.0.6** was hardened automatically. 5 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): Four `run:` blocks in action.yml directly interpolate GitHub Actions expressions inside shell commands. Specifically, `${{ fromJson(steps.get.outputs.response).metadata.id }}`, `${{ fromJson(steps.create.outputs.response).metadata.id }}`, `${{ fromJson(steps.update.outputs.response).metadata.parentId }}`, and `${{ fromJson(steps.delete.outputs.response).metadata.id }}` are all `steps.*.outputs.*` values (workflow-controllable) interpolated directly into shell variable assignments before the shell ever sees them, enabling command injection.

Locations:

- `action.yml:40`
- `action.yml:52`
- `action.yml:64`
- `action.yml:76`

### github-env-injection (severity: high)

Four `run:` blocks write values derived from `${{ fromJson(steps.*.outputs.response).metadata.* }}` (a `steps.*.outputs.*` — workflow-controllable context) into `$GITHUB_ENV` via an intermediate shell variable without any sanitization (`printf '%s' ... | tr -d '\n\r'`). An attacker-controlled HTTP response body could inject arbitrary environment variables into subsequent steps. Affected steps: GET, CREATE, UPDATE, and DELETE response handlers.

Locations:

- `action.yml:40`
- `action.yml:52`
- `action.yml:64`
- `action.yml:76`

### script-injection (severity: high)

Sub-rule (a): Multiple `run:` blocks in functional-tests.yml directly interpolate GitHub Actions expressions inside shell commands. Offending lines include: `expr length "${{ steps.jsonbin_create.outputs.bin_id }}"`, `${{ steps.jsonbin_create.outputs.url }}`, `jq -c '.record' <<< '${{ steps.http1.outputs.response }}'`, `${{ github.actor }}`, `curl ... ${{ steps.jsonbin_update.outputs.url }}`, and others. These `steps.*.outputs.*` and `github.*` values flow through YAML template substitution before the shell parses them, enabling command injection.

Locations:

- `.github/workflows/functional-tests.yml:24`
- `.github/workflows/functional-tests.yml:35`
- `.github/workflows/functional-tests.yml:47`
- `.github/workflows/functional-tests.yml:59`
- `.github/workflows/functional-tests.yml:71`
- `.github/workflows/functional-tests.yml:83`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to mutable tags or branch names instead of immutable 40-character commit SHAs, making the action vulnerable to supply-chain attacks if the referenced tag or branch is moved or compromised. Failing references in action.yml: `fjogeleit/http-request-action@v1.16.2` (4 occurrences). Failing references in functional-tests.yml: `actions/checkout@v4`, `fjogeleit/http-request-action@v1.16.2` (3 occurrences). Failing references in linting.yml: `fabasoad/reusable-workflows/...@main`. Failing references in release.yml: `fabasoad/reusable-workflows/...@bump/actionlint`. Failing references in security.yml: `fabasoad/reusable-workflows/...@main`. Failing references in sync-labels.yml: `fabasoad/reusable-workflows/...@main`. Failing references in update-license.yml: `fabasoad/reusable-workflows/...@main`.

Locations:

- `action.yml:30`
- `action.yml:43`
- `action.yml:56`
- `action.yml:68`
- `.github/workflows/functional-tests.yml:17`
- `.github/workflows/functional-tests.yml:27`
- `.github/workflows/functional-tests.yml:44`
- `.github/workflows/functional-tests.yml:67`
- `.github/workflows/linting.yml:12`
- `.github/workflows/release.yml:11`
- `.github/workflows/security.yml:14`
- `.github/workflows/sync-labels.yml:12`
- `.github/workflows/update-license.yml:11`

### missing-permissions (severity: medium)

Several workflow files have no top-level `permissions:` key and no job-level `permissions:` key on every job, meaning they run with the default (potentially broad) token permissions. Affected files: functional-tests.yml (job `functional-tests` has no permissions), linting.yml (job `pre-commit` has no permissions), release.yml (job `github` has no permissions), sync-labels.yml (job `maintenance` has no permissions), update-license.yml (job `maintenance` has no permissions). Note: security.yml passes because its single job has explicit job-level permissions.

Locations:

- `.github/workflows/functional-tests.yml:1`
- `.github/workflows/linting.yml:1`
- `.github/workflows/release.yml:1`
- `.github/workflows/sync-labels.yml:1`
- `.github/workflows/update-license.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, missing-permissions

**Notes:**

Fixed all findings across action.yml and .github/workflows/*.yml files:

1. script-injection + github-env-injection (action.yml lines 40,52,64,76): Moved all `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions from run: shell commands into env: blocks as RESPONSE variable, then sanitized with `printf '%s' "$RESPONSE" | tr -d '\n\r'` before writing to $GITHUB_ENV.

2. script-injection (functional-tests.yml lines 24,35,47,59,71,83): Moved all `${{ steps.*.outputs.* }}` and `${{ github.actor }}` expressions from run: shell commands into env: blocks (BIN_ID, BIN_URL, HTTP1_RESPONSE, HTTP2_RESPONSE, HTTP3_RESPONSE, ACTOR, BIN_URL).

3. unpinned-uses: Pinned fjogeleit/http-request-action@v1.16.2 to SHA 07eceb44a46c6fa1161bd89f97aeec4ec409bfc8, actions/checkout@v4 to SHA 11d5960a326750d5838078e36cf38b85af677262, and fabasoad/reusable-workflows@main to SHA c5bd8945762dab6d2f5168b65f10355887ea40a3 (used for all reusable workflow references including release.yml which referenced non-existent bump/actionlint branch).

4. missing-permissions: Added permissions blocks to functional-tests.yml (contents: read), linting.yml (contents: read), release.yml (contents: write), sync-labels.yml (contents: read + issues: write), and update-license.yml (contents: write).

### Iteration 2

**Fixes applied:** unpinned-uses

**Notes:**

Pinned the reusable workflow reference in .github/workflows/security.yml from `fabasoad/reusable-workflows/.github/workflows/wf-security-sast.yml@main` to `fabasoad/reusable-workflows/.github/workflows/wf-security-sast.yml@c5bd8945762dab6d2f5168b65f10355887ea40a3 # main` using the resolved commit SHA.

