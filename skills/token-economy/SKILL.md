---
name: token-economy
description: Token economy — trim tool outputs, answer terse with hard length caps, and don't reproduce large blocks. Use during any coding/agent task to cut output tokens (the expensive, model-controlled cost) without hurting correctness.
license: MIT
---

# Token economy rules

1. **Trim tool outputs to the few fields that matter** — never echo full logs or files back.
2. **Answer terse and structured, with hard caps** — ≤ N items, one sentence each, diff-only.
3. **Don't restate context or quote large blocks back** — reference by path/line, don't reproduce.
4. **Batch independent calls into one message** — reads, searches and checks that don't depend on each other go out together; one call per turn only when the next step needs the result.
5. **Read by range, not whole files** — `grep -n` first, then only the needed lines; a whole file only when the task needs all of it; don't re-read an unchanged file.
6. **One small screenshot per check** — scaled or zoomed for your own checks; full size only for QA evidence a human reviews.
7. **Send wide exploration to a subagent** — when finding the answer means reading more than ~50k tokens, let a subagent read and return only the conclusion; open the cited lines before acting on it.

Rules 4-7 shrink the context that every later call re-reads from cache.

For trivial one-liners, use judgment — brevity shouldn't cost correctness.
