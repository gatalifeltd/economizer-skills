# economizer-skills

**Token-economy guidelines for coding agents.** Drop-in rules that cut wasted context and
reduce the cost of agentic coding — for Claude Code, Codex, and Cursor.

Inspired by the format of [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills),
but aimed at a different problem: not *correctness*, but *cost*.

We tested this empirically — ~190 headless A/B runs across **Codex, Cursor/Composer, Claude
Opus 4.8 and Sonnet 4.6** (see **[FINDINGS.md](FINDINGS.md)**). The short version: a big
rules file doesn't save tokens (it's itself context, and modern agents are already frugal),
but a **tight 3-rule file cuts model output by 10–25% on Claude and Cursor** — and beats the
12-rule version on every agent. Less is more.

## The three golden rules

The validated, model-controllable core — this is what most people should use:

1. **Trim tool outputs to the few fields that matter** — never echo full logs or files back.
2. **Answer terse and structured, with hard caps** — ≤ N items, one sentence each, diff-only.
3. **Don't restate context or quote large blocks back** — reference, don't reproduce.

Best on output-heavy work (drafting, summaries, reviews, code generation, chat). See
[FINDINGS.md](FINDINGS.md) for the numbers and method.

## The full 12 rules (context)

The three golden rules are distilled from a longer list. Two tiers: **Tier A** is what the
agent does inside a session (the golden rules live here); **Tier B** is how the surrounding
workflow is built. Our tests showed Tier B can't be enacted by a file the model reads — it
belongs to whoever builds the agent loop (caching, model routing, context resets). Keep
Tier B as guidance for orchestration, not as agent instructions.

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

## From the makers

Built by the team behind **[Gatalife](https://gatalife.com/)** — check out our apps.

## License

[MIT](LICENSE).
