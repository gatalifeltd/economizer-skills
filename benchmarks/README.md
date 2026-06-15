# Benchmark

Does dropping the token-economy policy into a project actually cut tokens? This harness
A/B tests it across three agents.

## Design

```
tasks  ×  { WITH policy, WITHOUT policy }  ×  N reps  ×  { claude, codex, cursor }
```

The **only** difference between the two arms is whether the policy files
(`CLAUDE.md`, `AGENTS.md`, `.cursor/rules/token-economy.mdc`) are present in the task's
working directory. Same prompt, same model, same fixture otherwise.

Each run executes the agent **headless** in an isolated copy of the task fixture, and we
record tokens, cost, wall-clock, and exit status.

| Agent  | Invocation (headless)                                              | Token source            |
|--------|-------------------------------------------------------------------|-------------------------|
| Claude | `claude -p --output-format json --model <m>`                      | `.usage`, `.total_cost_usd` |
| Codex  | `codex exec --json -m <m>`                                        | usage event in stream   |
| Cursor | `cursor-agent -p --output-format json --model <m> --force`        | usage in result JSON    |

## Run it

```bash
# 1. Auth: claude & codex already logged in; cursor needs a one-time login:
cursor-agent login

# 2. Pin models (edit the top of run.sh), then sweep:
bash run.sh                 # full sweep
REPS=1 AGENTS=claude bash run.sh    # quick smoke test

# 3. Aggregate raw runs into the published table + chart:
python3 analyze.py
```

`run.sh` writes raw agent output to `runs/<id>.out` and one line per run to
`runs/manifest.jsonl`. `analyze.py` parses those, computes per-agent means and the
WITH-vs-WITHOUT reduction, and regenerates `RESULTS.md` + `chart.svg`.

## Tasks

Each `tasks/<name>/` has a `prompt.txt`, input fixture(s), and an optional `verify.sh`
(exit 0 = output acceptable). Tasks are chosen to exercise the **Tier-A** rules that a
single headless run can actually surface:

- `trim-log` — find a few lines in a large log (Rule 4: trim outputs)
- `extract-json` — reshape a verbose JSON payload (Rules 6, 11: deterministic transforms)
- `summarize` — bounded summary of a long doc (Rule 9: hard length limits)
- `grep-answer` — locate a definition across files (Rule 3: attach only what's needed)

## Honesty / limitations

Read these before trusting the numbers:

- **Single-session only.** This harness exercises **Tier A** (in-session behavior). The
  **Tier B** workflow rules (new session per task, model routing, plan/execute/review
  split, caching) are orchestration-level and are *not* measured here.
- **Small N + non-determinism.** Agents are stochastic; with small rep counts, differences
  inside the noise band are not meaningful. We report N and the spread, not just means.
- **Model/version drift.** Numbers are tied to the exact model versions and CLI versions
  on the run date — all recorded in `RESULTS.md`. They will move over time.
- **Provider accounting differs.** Token and cost definitions are not identical across
  Claude / Codex / Cursor (e.g. cache-read accounting). Compare each agent to *itself*
  across the two arms; cross-agent absolute numbers are indicative, not exact.
- **Raw output is committed** under `runs/` so anyone can re-parse and check our math.
