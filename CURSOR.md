# CURSOR.md

**Token economy — three rules** for Cursor (Composer / Agent). Output costs ~5× input and
input is mostly cached, so the cheapest win you control is a shorter, tighter response.
These cut Composer's output ~25% in our tests (see [FINDINGS.md](FINDINGS.md)).

## Install

Copy [`.cursor/rules/token-economy.mdc`](.cursor/rules/token-economy.mdc) into your
project's `.cursor/rules/`. With `alwaysApply: true` it loads into every session.

## The rules

1. **Trim tool outputs to the few fields that matter** — never echo full logs or files back.
2. **Answer terse and structured, with hard caps** — ≤ N items, one sentence each, diff-only.
3. **Don't restate context or quote large blocks back** — reference by path/line, don't reproduce.

For trivial one-liners, use judgment — brevity shouldn't cost correctness.

---

_From the makers — check out our apps at [gatalife.com](https://gatalife.com/)._
