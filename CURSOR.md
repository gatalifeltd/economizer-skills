# CURSOR.md

Token-economy guidelines for Cursor (Composer / Agent). These rules cut wasted context
and reduce the cost of long agent sessions.

## Install as a Cursor rule

Copy [`.cursor/rules/token-economy.mdc`](.cursor/rules/token-economy.mdc) into your
project's `.cursor/rules/` directory. With `alwaysApply: true` it loads into every
Composer/Agent session automatically. To scope it to certain files, set `globs` instead.

## The rules

**Tradeoff:** bias toward fewer, smaller, cheaper calls. For trivial one-shot edits the
overhead isn't worth it — use judgment.

### In-session (the agent does this)

1. **Compact active state.** Keep a short GOAL / CONSTRAINTS / DECISIONS / OPEN / NEXT
   block; update it rather than re-deriving context.
2. **Recent context only.** Collapse finished sub-tasks to one-line outcomes; drop stale
   tool output and dead plans.
3. **Only necessary files.** Read the minimum — targeted search + small slice over whole
   files. Don't `@`-attach files you won't act on.
4. **Trim tool outputs.** Keep the few fields that matter; never feed full logs/JSON back.
5. **Structured outputs, hard limits.** Fixed schemas with explicit caps ("≤ 5 bullets",
   "diff only").
6. **Deterministic code over model calls.** Mechanical transforms → a script/one-liner,
   not token-by-token reasoning.

### Workflow (how to run Cursor)

7. **New chat per task** — carry only the compact state forward, not the whole thread.
8. **Cache stable instructions/schemas** — keep the unchanging prefix put.
9. **Retrieval on a strict budget** — cap codebase context; more isn't more signal.
10. **Route simple steps to smaller models** — pick a cheaper model for
    classify/extract/short-rewrite; reserve the strongest for hard reasoning.
11. **Split plan / execute / review** into separate chats so each starts lean.
12. **Measure tokens per workflow**, rank by spend, fix the worst offender first.

---

**Working if:** context stays small across long sessions, outputs enter trimmed, mechanical
work is done by code, and cost-per-task trends down without quality dropping.

---

_From the makers — check out our apps at [gatalife.com](https://gatalife.com/)._
