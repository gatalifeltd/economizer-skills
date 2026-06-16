# economizer-skills

**Make your coding agent cheaper — without making it dumber.**

Three drop-in rules for Claude, Cursor, and Codex that cut the *expensive* part of the
bill: model output. Not vibes — [we measured it](FINDINGS.md): ~190 headless A/B runs
across **Claude Opus 4.8, Sonnet 4.6, Cursor/Composer 2.5, and Codex (gpt-5.5)**.

> **Why output?** Output tokens cost ~5× input, and input is mostly cache reads (~0.1×).
> So output is a wildly disproportionate share of the bill — **~40–45% of cost on Claude**
> despite being ~1.5% of the token count. Optimize the bill, not the token total.

Result: a tight 3-rule file **cuts model output 10–25% on Claude and Cursor** — and beats a
longer 12-rule version on *every* agent. Less really is more.

![output tokens saved by the 3-rule set](benchmarks/chart_min_output.svg)

_Output tokens by policy arm — green % is what the 3-rule "min" set saves vs no policy.
(Total token count is dominated by cheap cached input and barely moves — see
[FINDINGS.md](FINDINGS.md) for why output, not the total, is the number that matters.)_

## The three golden rules

1. **Trim tool outputs to the few fields that matter** — never echo full logs or files back.
2. **Answer terse and structured, with hard caps** — ≤ N items, one sentence each, diff-only.
3. **Don't restate context or quote large blocks back** — reference by path/line, don't reproduce.

> Best on output-heavy work: drafting, summaries, reviews, code generation, chat.
> For trivial one-liners, use judgment — brevity shouldn't cost correctness.

## Install

> Install **only the file for your tool** — you don't need several formats in one project.
> (This repo ships all three because it's the source; tools like Cursor auto-detect
> `CLAUDE.md`/`AGENTS.md` *and* `.cursor/rules`, so keeping them together just duplicates
> the same rules. One file per project is enough.)

### Claude Code (plugin)
```
/plugin marketplace add gatalifeltd/economizer-skills
/plugin install token-economy@economizer-skills
```
Or drop [`CLAUDE.md`](CLAUDE.md) into your repo root:
```bash
curl -O https://raw.githubusercontent.com/gatalifeltd/economizer-skills/main/CLAUDE.md
```

### Cursor (rule)
Copy [`.cursor/rules/token-economy.mdc`](.cursor/rules/token-economy.mdc) into your
project's `.cursor/rules/`. With `alwaysApply: true` it loads into every Composer/Agent
session automatically.

### Codex (AGENTS.md)
Drop [`AGENTS.md`](AGENTS.md) into your repo root (auto-read), or into `~/.codex/AGENTS.md`
to apply it globally:
```bash
curl -O https://raw.githubusercontent.com/gatalifeltd/economizer-skills/main/AGENTS.md
```

## Does it actually work?

Read the full story — hypothesis → 3 experiment series → numbers → conclusions — in
**[FINDINGS.md](FINDINGS.md)**. Output reduction with the minimal rules (vs no policy):

| Agent | output Δ |
|-------|---------:|
| Cursor / Composer 2.5 | **−24.6%** |
| Claude Opus 4.8 | **−21.7%** |
| Claude Sonnet 4.6 | **−8.8%** |
| Codex gpt-5.5 | −3.7% |

Reproduce it yourself: [`benchmarks/`](benchmarks/) (`bash run_min.sh && python3 analyze_min.py`).

## The longer story: 12 rules, and why only 3 ship

The three golden rules are distilled from a longer list of 12. They split into two tiers:

- **Tier A — in-session behavior the model can follow** (trim outputs, terse answers, read
  the minimum, deterministic code over LLM calls, compact running state). A file the model
  *reads* can influence these. The three golden rules are the subset that actually moved the
  needle in testing.
- **Tier B — orchestration the model can't do to itself** (new session per task, cache the
  stable prompt prefix, retrieval token budgets, route simple steps to a cheaper model,
  split plan/execute/review into separate calls, measure cost per workflow). These are
  decisions made by the *program* that runs the agent — they belong to whoever builds the
  loop, not in a file the model reads. Real, but out of scope for a drop-in rule.

The full 12-rule reference lives in [FINDINGS.md](FINDINGS.md).

## From the makers

Built by the team behind **[Gatalife](https://gatalife.com/)** — check out our apps.

## License

[MIT](LICENSE).
