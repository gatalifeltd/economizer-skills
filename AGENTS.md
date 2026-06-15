# AGENTS.md

**Token economy — three rules** (for Codex and any `AGENTS.md`-aware tool). Output costs
~5× input and input is mostly cached, so the cheapest win you control is a shorter, tighter
response. See [FINDINGS.md](FINDINGS.md). Merge with project rules.

1. **Trim tool outputs to the few fields that matter** — never echo full logs or files back.
   Extract with `grep`/`jq`/`--format`/`head`, then reason over the result, not the dump.
2. **Answer terse and structured, with hard caps** — ≤ N items, one sentence each,
   diff-only. No preamble, no restating the question.
3. **Don't restate context or quote large blocks back** — reference by path/line, don't
   reproduce.

For trivial one-liners, use judgment — brevity shouldn't cost correctness.

---

_From the makers — check out our apps at [gatalife.com](https://gatalife.com/)._
