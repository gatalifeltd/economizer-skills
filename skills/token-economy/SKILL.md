---
name: token-economy
description: Token economy — trim tool outputs, answer terse with hard length caps, and don't reproduce large blocks. Use during any coding/agent task to cut the most expensive, model-controlled cost (output tokens) without hurting correctness. Most effective on output-heavy work — drafting, summaries, reviews, code generation.
license: MIT
---

# Token Economy

Output tokens cost ~5× input, and input is mostly cached — so the cheapest win you control
is a shorter, tighter response. In ~190 A/B runs (Claude Opus/Sonnet, Cursor, Codex) these
three rules cut model output 10–25% on Claude and Cursor, beating a longer 12-rule version.

## The three rules

1. **Trim tool outputs to the few fields that matter.** Never echo full logs or files back —
   extract with `grep`/`jq`/`--format`/`head`, then reason over the result, not the dump.
2. **Answer terse and structured, with hard caps.** ≤ N items, one sentence each, diff-only.
   No preamble, no restating the question, no "here's my plan" filler.
3. **Don't restate context or quote large blocks back.** Reference by path/line; don't
   reproduce code the reader already has.

For trivial one-liners, use judgment — brevity shouldn't cost correctness.

The full 12-rule list (including orchestration-level rules for people *building* agent
loops) and the benchmark behind these three live in the repository's README and FINDINGS.md.
