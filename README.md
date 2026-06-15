# economizer-skills

**Token-economy guidelines for coding agents.** Drop-in rules that cut wasted context and
reduce the cost of agentic coding — for Claude Code, Codex, and Cursor.

Inspired by the format of [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills),
but aimed at a different problem: not *correctness*, but *cost*. Long agent sessions quietly
burn tokens by re-reading files, carrying stale history, pasting full tool outputs back into
context, and using a flagship model for mechanical work. These twelve rules fix the common
offenders.

> Backed by a reproducible A/B benchmark across three agents — see
> [`benchmarks/RESULTS.md`](benchmarks/RESULTS.md).

## The 12 rules

Two tiers. **Tier A** is what the agent does inside a session. **Tier B** is how the
surrounding workflow should be built.

**Tier A — in-session**
1. Maintain a compact active state (GOAL / CONSTRAINTS / DECISIONS / OPEN / NEXT).
2. Keep recent context only; summarize older history.
3. Attach only necessary files and tools.
4. Trim tool outputs to essential fields.
5. Use structured outputs with hard length limits.
6. Prefer deterministic code over model calls for mechanical transforms.

**Tier B — workflow**
7. Start a new session per task.
8. Cache stable instructions and repeated schemas.
9. Use retrieval with a strict token budget.
10. Route simple steps to smaller models.
11. Split planning, execution, and review into separate contexts.
12. Measure token cost per workflow; fix the worst offender first.

See [`CLAUDE.md`](CLAUDE.md) for the expanded rationale and [`EXAMPLES.md`](EXAMPLES.md)
for before/after pairs.

## Install

**Claude Code — per project:** drop [`CLAUDE.md`](CLAUDE.md) into your repo root.
```bash
curl -O https://raw.githubusercontent.com/gatalifeltd/economizer-skills/main/CLAUDE.md
```

**Claude Code — as a plugin/skill:** this repo ships a
[`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) exposing the
[`token-economy`](skills/token-economy/SKILL.md) skill.

**Codex (or any `AGENTS.md`-aware tool):** drop [`AGENTS.md`](AGENTS.md) into your repo root.
```bash
curl -O https://raw.githubusercontent.com/gatalifeltd/economizer-skills/main/AGENTS.md
```

**Cursor:** copy [`.cursor/rules/token-economy.mdc`](.cursor/rules/token-economy.mdc) into
your project's `.cursor/rules/`. See [`CURSOR.md`](CURSOR.md).

## Does it actually help?

We A/B test the rules: the same tasks run **with** and **without** the policy file, across
**Claude, Codex, and Cursor**, measuring tokens, cost, and whether the task still succeeds.
The harness and methodology (including its limitations) live in
[`benchmarks/`](benchmarks/); generated numbers in
[`benchmarks/RESULTS.md`](benchmarks/RESULTS.md).

## License

[MIT](LICENSE).
