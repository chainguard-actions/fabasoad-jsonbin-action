<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.6

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v2.0.6** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

All four `uses:` references in action.yml pin to the mutable version tag `@v1.16.2` instead of an immutable 40-character commit SHA. If the tag is moved or the upstream repository is compromised, the action will silently execute different code. Affected references: `fjogeleit/http-request-action@v1.16.2` (lines 36, 47, 57, 68).

Locations:

- `action.yml:36`
- `action.yml:47`
- `action.yml:57`
- `action.yml:68`

### script-injection (severity: high)

Four `run:` blocks directly interpolate `${{ ... }}` expressions from the `steps.*.outputs.*` context inside shell command strings (rule a). The values come from HTTP API responses parsed with `fromJson()` and are substituted verbatim into the shell before execution. A malicious or compromised API response could inject arbitrary shell commands. Offending lines:
- Line 42: `bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"`
- Line 53: `bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"`
- Line 64: `bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"`
- Line 75: `bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"`

Locations:

- `action.yml:42`
- `action.yml:53`
- `action.yml:64`
- `action.yml:75`

### github-env-injection (severity: high)

Four `run:` blocks write a value derived from `steps.*.outputs.*` (an untrusted-input source) to `$GITHUB_ENV` without the required sanitization step (`printf '%s' ... | tr -d '\n\r'`). In each case, the shell variable `bin_id` is populated from a `${{ fromJson(...) }}` expression and then written directly to `$GITHUB_ENV` via `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"`. A newline character embedded in the API response value could inject additional environment variables into subsequent steps.
- Lines 42-43 (GET branch)
- Lines 53-54 (CREATE branch)
- Lines 64-65 (UPDATE branch)
- Lines 75-76 (DELETE branch)

Locations:

- `action.yml:43`
- `action.yml:54`
- `action.yml:65`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed all three findings in hardened/action/action.yml:
1. unpinned-uses: Pinned all four `fjogeleit/http-request-action@v1.16.2` references to commit SHA `07eceb44a46c6fa1161bd89f97aeec4ec409bfc8` with the tag preserved as a comment.
2. script-injection: Moved all four `${{ fromJson(...) }}` expressions from inline shell strings into `env:` blocks (as `BIN_ID_RAW`), referenced safely as `$BIN_ID_RAW` in the shell.
3. github-env-injection: Added sanitization via `safe=$(printf '%s' "$BIN_ID_RAW" | tr -d '\n\r')` before writing to `$GITHUB_ENV` in all four run blocks, preventing newline-based environment variable injection.

