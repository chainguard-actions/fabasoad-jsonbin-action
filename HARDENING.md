<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.6

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **fabasoad--jsonbin-action/v2.0.6** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Four `run:` blocks in action.yml directly interpolate `${{ steps.*.outputs.* }}` expressions (via `fromJson(steps.*.outputs.response)`) into shell command strings. This is a sub-rule (a) violation: any `${{ ... }}` expression inside a `run:` block is a script-injection risk because the value is substituted by the YAML template engine before the shell ever sees it, allowing embedded shell metacharacters to be executed. Offending lines:
- Line 41: `bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"`
- Line 55: `bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"`
- Line 69: `bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"`
- Line 79: `bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"`

Locations:

- `action.yml:41`
- `action.yml:55`
- `action.yml:69`
- `action.yml:79`

### github-env-injection (severity: high)

Four `run:` blocks write a value derived from `${{ steps.*.outputs.* }}` expressions (HTTP API response data) to `$GITHUB_ENV` without the required sanitization step (`printf '%s' ... | tr -d '\n\r'`). The expression is first assigned to a shell variable `bin_id`, then echoed into `$GITHUB_ENV`. Routing through a shell variable does NOT sanitize the value — newline injection is still possible, allowing an attacker to inject arbitrary environment variables. Offending writes:
- Line 42: `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"` (GET block, bin_id from `${{ fromJson(steps.get.outputs.response).metadata.id }}`)
- Line 56: same pattern for CREATE block
- Line 70: same pattern for UPDATE block
- Line 80: same pattern for DELETE block

Locations:

- `action.yml:42`
- `action.yml:56`
- `action.yml:70`
- `action.yml:80`

### unpinned-uses (severity: high)

All four `uses:` references in action.yml pin to a version tag (`@v1.16.2`) rather than a full 40-character commit SHA. This means the action could be silently updated or replaced by a supply-chain attack without the consuming workflow noticing. Failing references:
- Line 35: `uses: fjogeleit/http-request-action@v1.16.2` (Get JSONbin step)
- Line 49: `uses: fjogeleit/http-request-action@v1.16.2` (Create JSONbin step)
- Line 63: `uses: fjogeleit/http-request-action@v1.16.2` (Update JSONbin step)
- Line 75: `uses: fjogeleit/http-request-action@v1.16.2` (Delete JSONbin step)

Locations:

- `action.yml:35`
- `action.yml:49`
- `action.yml:63`
- `action.yml:75`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed all three findings in action.yml:
1. unpinned-uses: Pinned all four `fjogeleit/http-request-action@v1.16.2` references to full SHA `07eceb44a46c6fa1161bd89f97aeec4ec409bfc8` with tag comment.
2. script-injection: Moved all four `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions out of `run:` shell strings into `env:` blocks as `BIN_ID_RAW`, referenced as plain `$BIN_ID_RAW` in the shell.
3. github-env-injection: Added `safe=$(printf '%s' "$BIN_ID_RAW" | tr -d '\n\r')` sanitization in all four `run:` blocks before writing to `$GITHUB_ENV`, preventing newline injection.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed the 'Set output' step in action.yml (line 95) to sanitize the inherited environment variable `$JSONBIN_ACTION_BIN_ID` before writing it to `$GITHUB_OUTPUT`. Added `safe=$(printf '%s' "$JSONBIN_ACTION_BIN_ID" | tr -d '\n\r')` and replaced both `echo` commands to use `$safe` instead of `${JSONBIN_ACTION_BIN_ID}` directly. This prevents API response data containing embedded newlines from injecting additional key-value pairs into the GitHub output file.

