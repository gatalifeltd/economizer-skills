---
name: token-economy
description: Token-economy guidelines to reduce wasted context and cut the cost of agentic coding. Use when running long agent sessions, processing large tool outputs, or designing multi-step agent workflows — to keep context small, trim outputs, prefer deterministic code, and route work to the cheapest sufficient model.
license: MIT
---

# Token Economy

Practical rules that lower the token cost of agentic coding without sacrificing quality.
Two tiers: **Tier A** is in-session behavior the agent executes directly; **Tier B** is
how the surrounding workflow should be designed.

## Tier A — In-session

1. **Compact active state** — keep a short GOAL / CONSTRAINTS / DECISIONS / OPEN / NEXT
   block; update it instead of re-deriving context.
2. **Recent context only** — collapse finished sub-tasks to one-line outcomes; drop stale
   tool output.
3. **Only necessary files & tools** — read the minimum; targeted grep + small slice over
   whole files.
4. **Trim tool outputs** — keep the few fields that matter; never feed full dumps back.
5. **Structured outputs with hard limits** — fixed schemas, explicit length caps.
6. **Deterministic code over model calls** — mechanical transforms go to a script.

## Tier B — Workflow

7. **New session per task** — carry only the compact state forward.
8. **Cache stable instructions & schemas** — pin the unchanging prefix.
9. **Retrieval on a strict token budget** — cap context; more isn't more signal.
10. **Route simple steps to smaller models** — reserve the flagship for hard reasoning.
11. **Split plan / execute / review** into separate contexts.
12. **Measure tokens per workflow** — rank by spend, fix the worst offender first.

See the repository's `CLAUDE.md` for the expanded rationale and `EXAMPLES.md` for
before/after comparisons. Benchmark numbers across Claude, Codex, and Cursor live in
`benchmarks/RESULTS.md`.
