<!-- markdownlint-disable -->

# Hardening Report: fabasoad--jsonbin-action/v2.0.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **fabasoad--jsonbin-action/v2.0.5** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Four `run:` blocks in action.yml directly interpolate `${{ fromJson(steps.*.outputs.response).metadata.* }}` expressions inside shell command strings (sub-rule a). These `steps.*.outputs.*` values originate from external HTTP API responses and are substituted by the YAML template engine before the shell parses them, allowing shell metacharacters in the API response to be interpreted as shell commands. Offending lines:
- Line 41: `bin_id="${{ fromJson(steps.get.outputs.response).metadata.id }}"`
- Line 54: `bin_id="${{ fromJson(steps.create.outputs.response).metadata.id }}"`
- Line 67: `bin_id="${{ fromJson(steps.update.outputs.response).metadata.parentId }}"`
- Line 79: `bin_id="${{ fromJson(steps.delete.outputs.response).metadata.id }}"`

Locations:

- `action.yml:41`
- `action.yml:54`
- `action.yml:67`
- `action.yml:79`

### github-env-injection (severity: high)

Four `run:` blocks write a value derived from `${{ fromJson(steps.*.outputs.response).metadata.* }}` (a `steps.*.outputs.*` expression — untrusted data from an external HTTP API) to `$GITHUB_ENV` without the required sanitization step (`printf '%s' ... | tr -d '\n\r'`). An attacker who can influence the JSONbin API response could inject arbitrary environment variables into subsequent steps via newline injection. Offending writes:
- Line 42: `echo "JSONBIN_ACTION_BIN_ID=${bin_id}" >> "$GITHUB_ENV"` (GET step, bin_id set from `${{ fromJson(steps.get.outputs.response).metadata.id }}`)
- Line 55: same pattern for CREATE step
- Line 68: same pattern for UPDATE step
- Line 80: same pattern for DELETE step

Locations:

- `action.yml:42`
- `action.yml:55`
- `action.yml:68`
- `action.yml:80`

### unpinned-uses (severity: high)

All four `uses:` references to `fjogeleit/http-request-action` are pinned to a mutable version tag (`@v1.15.2`) rather than an immutable 40-character SHA commit hash. A tag can be moved to point to a different (potentially malicious) commit, enabling a supply-chain attack. Failing references:
- `uses: fjogeleit/http-request-action@v1.15.2` (Get JSONbin step, line ~35)
- `uses: fjogeleit/http-request-action@v1.15.2` (Create JSONbin step, line ~47)
- `uses: fjogeleit/http-request-action@v1.15.2` (Update JSONbin step, line ~60)
- `uses: fjogeleit/http-request-action@v1.15.2` (Delete JSONbin step, line ~73)

Locations:

- `action.yml:35`
- `action.yml:47`
- `action.yml:60`
- `action.yml:73`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed all three findings in action.yml:
1. unpinned-uses: Pinned all four fjogeleit/http-request-action@v1.15.2 references to the immutable SHA 0bd00a33db6f82063a3c6befd41f232f61d66583, preserving the tag as a comment.
2. script-injection: Moved all four ${{ fromJson(steps.*.outputs.response).metadata.* }} expressions out of run: shell strings into env: blocks (as BIN_ID_RAW), referencing them as plain $BIN_ID_RAW environment variables in the shell.
3. github-env-injection: Added sanitization using printf '%s' "$BIN_ID_RAW" | tr -d '\n\r' before writing to $GITHUB_ENV in all four affected run: blocks, preventing newline injection attacks.

