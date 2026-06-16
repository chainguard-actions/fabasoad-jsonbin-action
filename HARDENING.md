<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **fabasoad--jsonbin-action/v2.0.3** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Four `run:` blocks in action.yml directly interpolate `${{ ... }}` expressions (specifically `steps.*.outputs.*` values from HTTP API responses) into shell commands, violating rule (a). An attacker who can influence the API response content could inject arbitrary shell commands. Offending lines:
- Line 41: `bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"`
- Line 55: `bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"`
- Line 69: `bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"`
- Line 82: `bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"`

Locations:

- `action.yml:41`
- `action.yml:55`
- `action.yml:69`
- `action.yml:82`

### github-env-injection (severity: high)

Four `run:` blocks write values derived from `steps.*.outputs.*` expressions (HTTP API response data) to `$GITHUB_ENV` without the required sanitization (`printf '%s' ... | tr -d '\n\r'`). The value is interpolated via `${{ fromJson(steps.*.outputs.response).metadata.* }}` into a shell variable and then written unsanitized to `$GITHUB_ENV`. Additionally, the 'Set output' step (line 90-91) writes the unsanitized `$JSONBIN_ACTION_BIN_ID` env var to `$GITHUB_OUTPUT` without sanitization. Offending steps:
- Line 42: `echo "JSONBIN_ACTION_BIN_ID=$bin_id" >> $GITHUB_ENV` (GET step)
- Line 56: `echo "JSONBIN_ACTION_BIN_ID=$bin_id" >> $GITHUB_ENV` (CREATE step)
- Line 70: `echo "JSONBIN_ACTION_BIN_ID=$bin_id" >> $GITHUB_ENV` (UPDATE step)
- Line 83: `echo "JSONBIN_ACTION_BIN_ID=$bin_id" >> $GITHUB_ENV` (DELETE step)
- Lines 90-91: `echo "bin_id=$JSONBIN_ACTION_BIN_ID" >> $GITHUB_OUTPUT` and `echo "url=.../$JSONBIN_ACTION_BIN_ID" >> $GITHUB_OUTPUT` (Set output step)

Locations:

- `action.yml:42`
- `action.yml:56`
- `action.yml:70`
- `action.yml:83`
- `action.yml:90`

### unpinned-uses (severity: high)

All four `uses:` references in action.yml use the mutable version tag `@v1.14.1` instead of a pinned 40-character SHA commit hash. This exposes the action to supply-chain attacks if the tag is moved or the upstream repository is compromised. Affected references:
- `uses: fjogeleit/http-request-action@v1.14.1` (GET step, line 35)
- `uses: fjogeleit/http-request-action@v1.14.1` (CREATE step, line 49)
- `uses: fjogeleit/http-request-action@v1.14.1` (UPDATE step, line 63)
- `uses: fjogeleit/http-request-action@v1.14.1` (DELETE step, line 76)

Locations:

- `action.yml:35`
- `action.yml:49`
- `action.yml:63`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed all three findings in action.yml:
1. unpinned-uses: Pinned all four `fjogeleit/http-request-action@v1.14.1` references to full SHA `eab8015483ccea148feff7b1c65f320805ddc2bf` with the tag preserved as a comment.
2. script-injection: Moved all four `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions out of `run:` shell strings into `env:` blocks (as `RESPONSE_BIN_ID`), then referenced them as plain environment variables in the shell scripts.
3. github-env-injection: Added `printf '%s' "$RESPONSE_BIN_ID" | tr -d '\n\r'` sanitization in all four GITHUB_ENV write steps, and similarly sanitized `$JSONBIN_ACTION_BIN_ID` before writing to `$GITHUB_OUTPUT` in the Set output step.

