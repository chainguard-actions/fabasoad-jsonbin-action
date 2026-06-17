<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **fabasoad--jsonbin-action/v2.0.4** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Four run: blocks in action.yml directly interpolate ${{ ... }} expressions (steps.*.outputs.* context values) inside shell command strings — sub-rule (a) violation. Specifically, each block assigns `bin_id="${{ fromJson(steps.*.outputs.response).metadata.* }}"` which causes GitHub Actions to perform YAML template substitution before the shell ever sees the value, allowing an attacker-controlled API response to inject arbitrary shell commands.

Locations:

- `action.yml:42`
- `action.yml:54`
- `action.yml:67`
- `action.yml:77`

### github-env-injection (severity: high)

Four run: blocks write a value derived from steps.*.outputs.* (via ${{ fromJson(steps.*.outputs.response).metadata.* }}) into $GITHUB_ENV without the required sanitization step (printf '%s' ... | tr -d '\n\r'). A newline embedded in the API response could inject arbitrary environment variable definitions into subsequent steps. The pattern `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"` appears in all four blocks without sanitization.

Locations:

- `action.yml:43`
- `action.yml:55`
- `action.yml:68`
- `action.yml:78`

### unpinned-uses (severity: high)

All four uses: references to fjogeleit/http-request-action use the mutable version tag @v1.15.1 instead of a full 40-character commit SHA. A tag can be moved to point to a different (potentially malicious) commit, enabling supply-chain attacks. Affected lines: `uses: fjogeleit/http-request-action@v1.15.1` (×4).

Locations:

- `action.yml:38`
- `action.yml:48`
- `action.yml:61`
- `action.yml:73`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed all three findings in action.yml:
1. unpinned-uses: Pinned all four fjogeleit/http-request-action@v1.15.1 references to full SHA @3fee9441848d10b67a3ee774ce26fbe8152a6c7a with # v1.15.1 comment.
2. script-injection: Moved all four ${{ fromJson(steps.*.outputs.response).metadata.* }} expressions from run: shell strings into env: blocks as BIN_ID_RAW, referencing $BIN_ID_RAW in the shell.
3. github-env-injection: Added sanitization in all four run: blocks using printf '%s' "$BIN_ID_RAW" | tr -d '\n\r' before writing to $GITHUB_ENV.

