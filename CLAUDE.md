# CLAUDE.md

**Token economy — three rules.** Output costs ~5× input and input is mostly cached, so the
cheapest win you control is a shorter, tighter response. These three cut output 10–25% on
Claude and Cursor in our tests (see [FINDINGS.md](FINDINGS.md)). Merge with project rules.

1. **Trim tool outputs to the few fields that matter** — never echo full logs or files back.
   Extract with `grep`/`jq`/`--format`/`head`, then reason over the result, not the dump.
2. **Answer terse and structured, with hard caps** — ≤ N items, one sentence each,
   diff-only. No preamble, no restating the question, no "here's what I'll do."
3. **Don't restate context or quote large blocks back** — reference by path/line, don't
   reproduce. The reader already has the code.

For trivial one-liners, use judgment — brevity shouldn't cost correctness.

---

_From the makers — check out our apps at [gatalife.com](https://gatalife.com/)._
