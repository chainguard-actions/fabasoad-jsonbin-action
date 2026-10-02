<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v2.0.3** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

All four `uses:` references in action.yml use the mutable version tag `@v1.14.1` instead of a pinned 40-character SHA commit hash. This exposes the action to supply-chain attacks if the tag is moved. Affected references: `fjogeleit/http-request-action@v1.14.1` (lines 37, 50, 64, 78).

Locations:

- `action.yml:37`
- `action.yml:50`
- `action.yml:64`
- `action.yml:78`

### script-injection (severity: high)

Rule (a): Four `run:` blocks directly interpolate `${{ ... }}` expressions inside shell command strings. Specifically, each block assigns `bin_id="${{ fromJson(steps.*.outputs.response).metadata.* }}"` — embedding a `steps.*.outputs.*` expression directly into the shell script before the shell ever sees it. If the API response contains shell metacharacters, this allows command injection. Offending lines: line 44 (`${{ fromJson(steps.get.outputs.response).metadata.id }}`), line 58 (`${{ fromJson(steps.create.outputs.response).metadata.id }}`), line 72 (`${{ fromJson(steps.update.outputs.response).metadata.parentId }}`), line 85 (`${{ fromJson(steps.delete.outputs.response).metadata.id }}`).

Locations:

- `action.yml:44`
- `action.yml:58`
- `action.yml:72`
- `action.yml:85`

### github-env-injection (severity: high)

Four `run:` blocks write values derived from `steps.*.outputs.*` (untrusted step output data from the JSONbin API response) into `$GITHUB_ENV` without the required sanitization step (`printf '%s' ... | tr -d '\n\r'`). An attacker-controlled API response containing newlines could inject arbitrary environment variables. Additionally, the 'Set output' step (line 92-93) writes `$JSONBIN_ACTION_BIN_ID` — which was set from these unsanitized step outputs — to `$GITHUB_OUTPUT` without sanitization. Affected writes to $GITHUB_ENV: lines 45, 59, 73, 86. Affected writes to $GITHUB_OUTPUT: lines 92-93.

Locations:

- `action.yml:45`
- `action.yml:59`
- `action.yml:73`
- `action.yml:86`
- `action.yml:92`
- `action.yml:93`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed all three findings in hardened/action/action.yml:
1. unpinned-uses: Pinned all four fjogeleit/http-request-action@v1.14.1 references to SHA eab8015483ccea148feff7b1c65f320805ddc2bf with the tag preserved as a comment.
2. script-injection: Moved all four ${{ fromJson(steps.*.outputs.response).metadata.* }} expressions out of run: shell strings into env: blocks (GET_RESPONSE, CREATE_RESPONSE, UPDATE_RESPONSE, DELETE_RESPONSE), referencing them as plain shell variables.
3. github-env-injection: Added printf '%s' ... | tr -d '\n\r' sanitization before all four writes to $GITHUB_ENV, and also sanitized $JSONBIN_ACTION_BIN_ID before writing to $GITHUB_OUTPUT in the Set output step.

