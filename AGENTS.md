# AGENTS.md

Token-economy guidelines for coding agents (Codex, and any tool that reads `AGENTS.md`).
The goal is fewer, smaller, cheaper model calls without losing quality. Merge with
project-specific instructions as needed.

**Tradeoff:** These rules bias toward economy over convenience. For trivial one-shot
tasks the overhead isn't worth it — use judgment.

Two tiers: **Tier A** is in-session behavior the agent executes directly; **Tier B** is
how the surrounding workflow should be designed (follow when you orchestrate, recommend
otherwise).

---

## Tier A — In-session behavior

1. **Maintain a compact active state.** Keep a short block — GOAL / CONSTRAINTS /
   DECISIONS / OPEN / NEXT — and update it instead of re-deriving context from history.

2. **Keep recent context only; summarize older history.** When a sub-task finishes,
   collapse its details to a one-line outcome and drop stale tool output and dead plans.

3. **Attach only necessary files and tools.** Read the minimum needed to act — a targeted
   grep and a small slice beat reading whole files "for context."

4. **Trim tool outputs to essential fields.** Extract the few fields that matter
   (`jq`/`grep`/`--format`/`head`); never feed a full log or full JSON back into reasoning.

5. **Use structured outputs with hard length limits.** Prefer JSON/fixed schemas with
   explicit caps ("≤ 5 bullets", "diff only"). Open-ended answers are a silent token sink.

6. **Prefer deterministic code over model calls.** For mechanical transforms — reformat,
   extract, find/replace, count, sort — write a script/one-liner instead of reasoning
   through it. Reserve model calls for real judgment.

---

## Tier B — Workflow & orchestration

7. **Start a new session per task.** Carry forward only the compact state block, not the
   full transcript.

8. **Cache stable instructions and repeated schemas.** Pin the unchanging prompt prefix;
   don't re-send it every turn.

9. **Use retrieval with a strict token budget.** Cap retrieved context (top-k + token
   ceiling); more retrieved text is not more signal.

10. **Route simple steps to smaller models.** Send classification/extraction/short
    rewrites to a cheaper tier; reserve the flagship for hard reasoning.

11. **Split planning, execution, and review into separate contexts.** Each starts lean
    instead of one bloated do-everything context.

12. **Measure token cost per workflow; fix the worst offender first.** Track tokens per
    workflow, rank by spend, attack the top consumer.

---

**Working if:** context stays small across long tasks, tool outputs enter reasoning
trimmed, mechanical work is done by code, and cost-per-task trends down without quality
dropping.

---

_From the makers — check out our apps at [gatalife.com](https://gatalife.com/)._
