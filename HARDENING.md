<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v2.0.3** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): Four `run:` blocks in action.yml directly interpolate `${{ }}` expressions inside shell commands. Specifically, each block assigns `bin_id="${{ fromJson(steps.*.outputs.response).metadata.* }}"` — a step output value — directly into the shell script via YAML template substitution before the shell ever sees it. This allows an attacker-controlled API response to inject arbitrary shell commands. Offending lines: `bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"`, `bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"`, `bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"`, `bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"`.

Locations:

- `action.yml:43`
- `action.yml:55`
- `action.yml:68`
- `action.yml:78`

### github-env-injection (severity: high)

Four `run:` blocks in action.yml write a value derived from `steps.*.outputs.*` (an untrusted, workflow-controllable source) to `$GITHUB_ENV` without the required sanitization step (`printf '%s' ... | tr -d '\n\r'`). Each block sets `bin_id` from a `${{ fromJson(...) }}` expression and then writes `echo "JSONBIN_ACTION_BIN_ID=$bin_id" >> $GITHUB_ENV`. A newline in the response value could inject arbitrary environment variables into subsequent steps.

Locations:

- `action.yml:44`
- `action.yml:56`
- `action.yml:69`
- `action.yml:79`

### unpinned-uses (severity: high)

action.yml references `fjogeleit/http-request-action@v1.14.1` four times using a mutable version tag instead of a full 40-character commit SHA. A tag can be moved to point to a different (potentially malicious) commit at any time, enabling supply-chain attacks.

Locations:

- `action.yml:30`
- `action.yml:44`
- `action.yml:57`
- `action.yml:68`

### unpinned-uses (severity: high)

All four workflow files use mutable tag/branch refs instead of pinned 40-character commit SHAs. Unpinned references: functional-tests.yml: `actions/checkout@v3`, `fjogeleit/http-request-action@v1.14.1` (×3); pre-commit.yml: `actions/checkout@v3`, container image `ghcr.io/fabasoad/pre-commit-container:latest` (mutable tag); release.yml: `actions/checkout@v3`, `simbo/changes-since-last-release-action@v1`, `softprops/action-gh-release@v1`, `fischerscode/tagger@v0`; update-license.yml: `actions/checkout@v3`, `FantasticFiasco/action-update-license-year@v3`.

Locations:

- `.github/workflows/functional-tests.yml:15`
- `.github/workflows/functional-tests.yml:28`
- `.github/workflows/functional-tests.yml:47`
- `.github/workflows/functional-tests.yml:67`
- `.github/workflows/pre-commit.yml:20`
- `.github/workflows/release.yml:13`
- `.github/workflows/release.yml:18`
- `.github/workflows/release.yml:22`
- `.github/workflows/release.yml:30`
- `.github/workflows/update-license.yml:11`
- `.github/workflows/update-license.yml:12`

### missing-permissions (severity: medium)

None of the four workflow files define a top-level `permissions:` key, and none of the jobs within them define job-level `permissions:` keys. Without explicit permissions, workflows run with the default (often broad) token permissions, violating the principle of least privilege.

Locations:

- `.github/workflows/functional-tests.yml:1`
- `.github/workflows/pre-commit.yml:1`
- `.github/workflows/release.yml:1`
- `.github/workflows/update-license.yml:1`

### script-injection (severity: high)

Sub-rule (a): Multiple `run:` blocks in workflow files directly interpolate `${{ }}` expressions inside shell commands. In functional-tests.yml: `[[ "$(jq -c '.record' <<< '${{ steps.http1.outputs.response }}')" == ... ]]` and `[[ $(curl ... ${{ steps.jsonbin_update.outputs.url }}) ... ]]` inject step outputs directly into shell. In pre-commit.yml: `pre-commit run --to-ref ${{ github.sha }} --from-ref origin/${{ github.base_ref }}` injects github context values directly into shell commands. These bypass shell quoting and allow injection of shell metacharacters.

Locations:

- `.github/workflows/functional-tests.yml:33`
- `.github/workflows/functional-tests.yml:57`
- `.github/workflows/functional-tests.yml:75`
- `.github/workflows/functional-tests.yml:88`
- `.github/workflows/functional-tests.yml:100`
- `.github/workflows/pre-commit.yml:28`
- `.github/workflows/pre-commit.yml:33`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, missing-permissions

**Notes:**

Fixed all findings across action.yml and four workflow files:

1. action.yml - script-injection & github-env-injection: Moved all four `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions into `env:` blocks as `RESPONSE_BIN_ID`. Added sanitization with `printf '%s' "$RESPONSE_BIN_ID" | tr -d '\n\r'` before writing to `$GITHUB_ENV`.

2. action.yml - unpinned-uses: Pinned `fjogeleit/http-request-action@v1.14.1` to SHA `eab8015483ccea148feff7b1c65f320805ddc2bf` (×4).

3. functional-tests.yml: Added `permissions: contents: read`; pinned `actions/checkout@v3` and `fjogeleit/http-request-action@v1.14.1` (×3) to full SHAs; moved all `${{ steps.*.outputs.* }}` and `${{ github.actor }}` expressions in run blocks to env: blocks.

4. pre-commit.yml: Added `permissions: contents: read`; pinned `actions/checkout@v3` to full SHA; pinned container image with digest; moved `${{ github.sha }}` and `${{ github.base_ref }}` to env: block.

5. release.yml: Added `permissions: contents: write`; pinned all four actions to full SHAs.

6. update-license.yml: Added `permissions: contents: write, pull-requests: write`; pinned both actions to full SHAs.

