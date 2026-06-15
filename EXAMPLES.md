# EXAMPLES

Before/after pairs showing each rule in practice. The "after" column is what the rules ask
for — and what cuts tokens.

## Rule 4 — Trim tool outputs

A 2,000-line log and the 5 lines you need cost very different amounts.

**Before** — full dump into context:
```
cat server.log        # 2,000 lines streamed back, reasoned over in full
```

**After** — extract first, reason over the result:
```
grep -E "ERROR|FATAL" server.log | tail -5
```
> Pull the failing lines; never paste the whole file back.

## Rule 6 / 11 — Deterministic code over model calls

**Before** — ask the model to reshape JSON token-by-token:
> "Here's a 500-line API response, please extract every user's id and email and give me a list."

**After** — let `jq` do it for free and deterministically:
```
jq -r '.users[] | "\(.id)\t\(.email)"' response.json
```
> The transform is mechanical. A one-liner is cheaper, exact, and reproducible.

## Rule 1 — Compact active state

**Before** — re-explaining the whole task each turn, re-reading files to "remember":
> "So, recapping everything we've done: first we looked at the auth module, then we
> discussed three options for token refresh, and you suggested... let me re-read auth.ts
> to check where we were..."

**After** — a state block you update in place:
```
GOAL:        add silent token refresh to auth.ts
CONSTRAINTS: no new deps; keep existing AuthContext API
DECISIONS:   use refresh-on-401 interceptor (option B)
OPEN:        where to store the refresh token?
NEXT:        write the interceptor + a failing test
```

## Rule 9 — Structured outputs with hard limits

**Before:**
> "Explain everything you found about the performance issue."
> → three paragraphs, much of it restated context.

**After:**
> "Return JSON: `{cause: string (≤1 sentence), file: string, fix: string (≤2 sentences)}`."
> → bounded, parseable, no padding.

## Rule 3 — Start a new session per task

**Before** — one 300-message thread covering a bugfix, a refactor, and a docs update; every
new question re-reads the entire history.

**After** — three sessions, each seeded with only the compact state it needs. The docs
session never pays for the bugfix transcript.

## Rule 8 — Route simple steps to smaller models

**Before** — the flagship model classifies "is this a bug report or a feature request?"
for every issue.

**After** — a cheap/fast model handles the classification; the flagship is reserved for
actually fixing the bug. Same result, a fraction of the cost.
