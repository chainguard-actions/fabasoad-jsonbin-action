<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v2.0.5** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): Four run: blocks in action.yml directly interpolate ${{ fromJson(steps.*.outputs.response).metadata.* }} expressions inside shell command strings. Step-output values are workflow-controllable and flow through YAML template substitution before the shell sees them, enabling command injection. Offending lines include:
  bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"
  bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"
  bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"
  bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"

Locations:

- `action.yml:36`
- `action.yml:52`
- `action.yml:68`
- `action.yml:84`

### github-env-injection (severity: high)

Four run: blocks in action.yml write values derived from ${{ fromJson(steps.*.outputs.response).metadata.* }} (step outputs — workflow-controllable) directly to $GITHUB_ENV without the required sanitization step (printf '%s' ... | tr -d '\n\r'). This allows an attacker to inject arbitrary environment variables or override existing ones by embedding newlines in the API response. Offending pattern in each block:
  bin_id="${{ fromJson(steps.*.outputs.response).metadata.* }}"
  echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"

Locations:

- `action.yml:37`
- `action.yml:53`
- `action.yml:69`
- `action.yml:85`

### script-injection (severity: high)

Sub-rule (a): Multiple run: blocks in functional-tests.yml directly interpolate ${{ steps.*.outputs.* }} and ${{ github.actor }} expressions inside shell command strings. These values flow through YAML template substitution before the shell processes them, enabling command injection. Offending lines include:
  [[ $(expr length "${{ steps.jsonbin_create.outputs.bin_id }}") -eq 0 ]]
  [[ "${{ steps.jsonbin_create.outputs.url }}" == ... ]]
  [[ "$(jq -c '.record' <<< '${{ steps.http1.outputs.response }}')" == '{"running_by":"${{ github.actor }}"}' ]]
  [[ $(curl -s -o /dev/null -w "%{http_code}" ${{ steps.jsonbin_update.outputs.url }}) -eq 404 ]]

Locations:

- `.github/workflows/functional-tests.yml:26`
- `.github/workflows/functional-tests.yml:38`
- `.github/workflows/functional-tests.yml:50`
- `.github/workflows/functional-tests.yml:62`
- `.github/workflows/functional-tests.yml:74`
- `.github/workflows/functional-tests.yml:86`

### unpinned-uses (severity: high)

action.yml references fjogeleit/http-request-action@v1.15.2 four times using a version tag instead of a full 40-character commit SHA. A tag can be moved to point to a different (potentially malicious) commit, enabling supply-chain attacks.

Locations:

- `action.yml:29`
- `action.yml:45`
- `action.yml:61`
- `action.yml:77`

### unpinned-uses (severity: high)

All uses: references across workflow files use mutable tags or branch names instead of pinned 40-character commit SHAs. Affected references include: actions/checkout@v4, fjogeleit/http-request-action@v1.15.2, fabasoad/reusable-workflows/...@main, simbo/changes-since-last-release-action@v1, softprops/action-gh-release@v2, fischerscode/tagger@v0, github/codeql-action/init@v3, github/codeql-action/analyze@v3, github/codeql-action/upload-sarif@v3, anchore/scan-action@v3, micnncim/action-label-syncer@v1, FantasticFiasco/action-update-license-year@v3.

Locations:

- `.github/workflows/functional-tests.yml:17`
- `.github/workflows/functional-tests.yml:31`
- `.github/workflows/functional-tests.yml:43`
- `.github/workflows/functional-tests.yml:55`
- `.github/workflows/linting.yml:12`
- `.github/workflows/release.yml:14`
- `.github/workflows/release.yml:19`
- `.github/workflows/release.yml:22`
- `.github/workflows/release.yml:28`
- `.github/workflows/security.yml:17`
- `.github/workflows/security.yml:19`
- `.github/workflows/security.yml:22`
- `.github/workflows/security.yml:26`
- `.github/workflows/security.yml:33`
- `.github/workflows/security.yml:36`
- `.github/workflows/security.yml:40`
- `.github/workflows/sync-labels.yml:17`
- `.github/workflows/sync-labels.yml:20`
- `.github/workflows/update-license.yml:12`
- `.github/workflows/update-license.yml:15`

### missing-permissions (severity: medium)

None of the workflow files define a top-level permissions: key, and no job within any workflow defines a job-level permissions: key. Without explicit permissions, workflows run with the default (potentially write-all) token permissions, violating the principle of least privilege.

Locations:

- `.github/workflows/functional-tests.yml:1`
- `.github/workflows/linting.yml:1`
- `.github/workflows/release.yml:1`
- `.github/workflows/security.yml:1`
- `.github/workflows/sync-labels.yml:1`
- `.github/workflows/update-license.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, missing-permissions

**Notes:**

Fixed all findings across action.yml and all 6 workflow files:

1. script-injection (action.yml): Moved all ${{ fromJson(steps.*.outputs.response).metadata.* }} expressions into env: blocks (BIN_ID_RAW) and referenced as $BIN_ID_RAW in shell scripts.

2. github-env-injection (action.yml): Added sanitization with `printf '%s' "$BIN_ID_RAW" | tr -d '\n\r'` before writing to $GITHUB_ENV in all 4 affected blocks.

3. script-injection (functional-tests.yml): Moved all ${{ steps.*.outputs.* }} and ${{ github.actor }} expressions into env: blocks and referenced as plain env vars in shell scripts.

4. unpinned-uses (action.yml): Pinned fjogeleit/http-request-action@v1.15.2 to SHA 0bd00a33db6f82063a3c6befd41f232f61d66583 in all 4 occurrences.

5. unpinned-uses (workflow files): Pinned all 12 action references across all workflow files to their full 40-character commit SHAs with tag comments for readability.

6. missing-permissions: Added top-level permissions blocks to all 6 workflow files with minimal required permissions (contents:read for most, plus security-events:write for security.yml, issues:write for sync-labels.yml, contents:write and pull-requests:write for update-license.yml, contents:write for release.yml).

