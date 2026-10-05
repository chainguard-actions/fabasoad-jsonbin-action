<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **fabasoad--jsonbin-action/v2.0.5** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Four `run:` blocks in action.yml directly interpolate `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions inside shell commands (rule a). `steps.*.outputs.*` is a workflow-controllable context, and any `${{ ... }}` inside a `run:` block is a script injection risk — the value is substituted by the Actions runner before the shell ever sees it, allowing an attacker-controlled API response to inject arbitrary shell commands. Offending lines:
- Line 40: `bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"`
- Line 53: `bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"`
- Line 66: `bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"`
- Line 77: `bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"`

Locations:

- `action.yml:40`
- `action.yml:53`
- `action.yml:66`
- `action.yml:77`

### github-env-injection (severity: high)

Four `run:` blocks write a value derived from `steps.*.outputs.*` (an untrusted, workflow-controllable source) to `$GITHUB_ENV` without the required sanitization step (`printf '%s' ... | tr -d '\n\r'`). In each block, `${{ fromJson(steps.*.outputs.response).metadata.* }}` is assigned to the shell variable `bin_id`, which is then written directly to `$GITHUB_ENV`. A newline character in the API response value could allow an attacker to inject arbitrary environment variable definitions into subsequent steps. Offending writes:
- Line 41: `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"` (GET block)
- Line 54: `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"` (CREATE block)
- Line 67: `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"` (UPDATE block)
- Line 78: `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"` (DELETE block)

Locations:

- `action.yml:41`
- `action.yml:54`
- `action.yml:67`
- `action.yml:78`

### unpinned-uses (severity: high)

All four `uses:` references in action.yml pin to a mutable version tag (`@v1.15.2`) rather than an immutable 40-character SHA commit hash. If the tag is moved (intentionally or via a supply-chain compromise), the action will silently execute different code. Failing references:
- Line 35: `uses: fjogeleit/http-request-action@v1.15.2`
- Line 46: `uses: fjogeleit/http-request-action@v1.15.2`
- Line 59: `uses: fjogeleit/http-request-action@v1.15.2`
- Line 72: `uses: fjogeleit/http-request-action@v1.15.2`
Fix: pin each to the full SHA, e.g. `uses: fjogeleit/http-request-action@<40-char-sha> # v1.15.2`.

Locations:

- `action.yml:35`
- `action.yml:46`
- `action.yml:59`
- `action.yml:72`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection, unpinned-uses

**Notes:**

Fixed all three findings in hardened/action/action.yml:
1. unpinned-uses: Pinned all four `fjogeleit/http-request-action@v1.15.2` references to SHA `0bd00a33db6f82063a3c6befd41f232f61d66583` with the tag preserved as a comment.
2. script-injection: Moved all four `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions out of `run:` shell strings and into `env:` blocks as `BIN_ID_RAW`, referenced via `$BIN_ID_RAW` in the shell.
3. github-env-injection: Added `printf '%s' "$BIN_ID_RAW" | tr -d '\n\r'` sanitization in all four blocks before writing to `$GITHUB_ENV`, preventing newline injection.

