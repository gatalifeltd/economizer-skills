# CLAUDE.md

Token-economy guidelines to reduce wasted context and cut the cost of agentic coding.
Merge with project-specific instructions as needed.

**Tradeoff:** These rules bias toward fewer, smaller, cheaper model calls. For trivial
one-shot tasks the overhead of managing state isn't worth it — use judgment.

The rules come in two tiers. **Tier A** is what you, the agent, do inside a session.
**Tier B** is how the surrounding workflow should be built — follow it when you control
orchestration, and recommend it when you don't.

---

## Tier A — In-session behavior

### 1. Maintain a compact active state

Keep a short running block — not prose — and update it instead of re-deriving context:

```
GOAL:        <one line>
CONSTRAINTS: <hard limits>
DECISIONS:   <what's settled, so you don't reopen it>
OPEN:        <unresolved questions>
NEXT:        <the single next action>
```

If you can answer from this block, don't re-read files to rebuild it.

### 2. Keep recent context only; summarize older history

Once a sub-task is done, replace its blow-by-blow with a one-line outcome. Don't carry
stale tool output, superseded plans, or abandoned branches forward. Summarize, then drop.

### 5. Attach only necessary files and tools

Read the minimum needed to act. Prefer a targeted grep + a 20-line slice over reading a
whole file. Don't open files "for context" on a hunch — open them when an action depends
on their contents.

### 6. Trim tool outputs to essential fields

Never paste a full log, full JSON, or full HTML back into reasoning. Extract the 3–5
fields that matter (`jq`, `grep`, `--format`, `head`) and discard the rest. A 2,000-line
dump and its 5 relevant lines cost very different amounts — pay for the 5.

### 9. Use structured outputs with hard length limits

Ask for (and produce) JSON / fixed schemas with explicit caps: "≤ 5 bullets", "one
sentence", "diff only". Open-ended "explain everything" answers are the most common
silent token sink.

### 11. Prefer deterministic code over LLM calls

For anything mechanical — reformatting, field extraction, find/replace, counting, sorting
— write a `sed`/`jq`/script one-liner instead of reasoning token-by-token through it.
Deterministic, free, and reproducible. Reserve model calls for genuine judgment.

---

## Tier B — Workflow & orchestration

### 3. Start a new session per task

Don't let one long-lived context accumulate ten unrelated tasks. Fresh task → fresh
session. Carry forward only the compact state block (Rule 1), not the transcript.

### 4. Cache stable instructions and repeated schemas

System prompts, style guides, and schemas that don't change between calls belong in a
prompt cache, not re-sent every turn. Identify the stable prefix and pin it.

### 7. Retrieval with a strict token budget

When using RAG/search, cap retrieved context (e.g. top-k with a token ceiling) rather
than dumping every match. More retrieved text is not more signal.

### 8. Route simple steps to smaller models

Classification, extraction, routing, and short rewrites don't need your largest model.
Send them to a cheaper tier; reserve the flagship for hard reasoning. If you can't switch
your own model, say which steps should be downgraded.

### 10. Split planning, execution, and review into separate contexts

A bloated do-everything context is expensive and error-prone. Plan in one context, hand a
compact spec to execution, review in a third. Each starts lean.

### 12. Measure token cost per workflow; fix the worst offender first

You can't optimize what you don't measure. Track tokens per workflow, rank by spend, and
attack the top consumer. Most savings come from one or two hotspots.

---

**These guidelines are working if:** context stays small across long tasks, tool outputs
enter reasoning trimmed not raw, mechanical work is done by code not tokens, and your
cost-per-task trends down without quality dropping.

---

_From the makers — check out our apps at [gatalife.com](https://gatalife.com/)._
