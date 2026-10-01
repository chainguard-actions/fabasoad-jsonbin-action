<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v2.0.4** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

All four `uses:` references in action.yml pin to a mutable tag (`v1.15.1`) rather than a full 40-character commit SHA. This means the action can be silently updated to a different (potentially malicious) version without any change to the workflow file. Affected lines: `uses: fjogeleit/http-request-action@v1.15.1` (appears 4 times — for GET, CREATE, UPDATE, and DELETE steps). Each should be pinned to a full SHA, e.g. `uses: fjogeleit/http-request-action@<40-char-sha> # v1.15.1`.

Locations:

- `action.yml:33`
- `action.yml:46`
- `action.yml:57`
- `action.yml:68`

### script-injection (severity: high)

Sub-rule (a): Four `run:` blocks directly interpolate `${{ ... }}` expressions into shell command strings. Specifically, each block assigns `bin_id="${{ fromJson(steps.<id>.outputs.response).metadata.id }}"` (or `.parentId`). The `steps.*.outputs.*` context is workflow-controllable and flows through YAML template substitution before the shell sees it, allowing an attacker to inject arbitrary shell metacharacters. The offending lines are:
- GET step: `bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"`
- CREATE step: `bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"`
- UPDATE step: `bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"`
- DELETE step: `bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"`

Sub-rule (b): The final "Set output" step uses `${JSONBIN_ACTION_BIN_ID}` unquoted inside a URL string: `echo "url=https://api.jsonbin.io/v3/b/${JSONBIN_ACTION_BIN_ID}"`. This env var holds a value originally sourced from the untrusted `steps.*.outputs.*` context and must be double-quoted.

Locations:

- `action.yml:38`
- `action.yml:51`
- `action.yml:62`
- `action.yml:73`
- `action.yml:84`

### github-env-injection (severity: high)

Four `run:` blocks write a value derived from `${{ fromJson(steps.*.outputs.response).metadata.* }}` (an untrusted `steps.*.outputs.*` expression) to `$GITHUB_ENV` without the required sanitization step (`printf '%s' ... | tr -d '\n\r'`). An attacker who can influence the HTTP response body could inject newlines to set arbitrary environment variables for subsequent steps.

Affected pattern in each block:
```
bin_id="${{ fromJson(steps.<id>.outputs.response).metadata.id }}"
echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"
```

Additionally, the final "Set output" step writes `${JSONBIN_ACTION_BIN_ID}` (which was set from the same untrusted source via `$GITHUB_ENV`) to `$GITHUB_OUTPUT` without sanitization:
```
echo "bin_id=${JSONBIN_ACTION_BIN_ID}" >> "$GITHUB_OUTPUT"
echo "url=https://api.jsonbin.io/v3/b/${JSONBIN_ACTION_BIN_ID}" >> "$GITHUB_OUTPUT"
```
All writes must be preceded by `safe=$(printf '%s' "$VAR" | tr -d '\n\r')` before writing to the special environment files.

Locations:

- `action.yml:39`
- `action.yml:52`
- `action.yml:63`
- `action.yml:74`
- `action.yml:84`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed all three findings in hardened/action/action.yml:

1. unpinned-uses: Pinned all four `fjogeleit/http-request-action@v1.15.1` references to the full SHA `3fee9441848d10b67a3ee774ce26fbe8152a6c7a` with the tag preserved as a comment.

2. script-injection: Moved all four `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions out of `run:` shell strings and into `env:` blocks as `BIN_ID_RAW`, referenced as plain shell variable `$BIN_ID_RAW` in the scripts.

3. github-env-injection: Added `safe=$(printf '%s' "$BIN_ID_RAW" | tr -d '\n\r')` sanitization before every write to `$GITHUB_ENV` (in all four method-specific steps) and before writes to `$GITHUB_OUTPUT` in the final 'Set output' step, preventing newline injection attacks.

