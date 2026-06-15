#!/usr/bin/env bash
# A/B token-economy benchmark harness.
#
#   tasks × {with,without} policy × REPS × agents
#
# Writes raw agent output to runs/<id>.out and one manifest line per run to
# runs/manifest.jsonl. Parsing of tokens/cost happens in analyze.py (one place,
# easy to fix per-agent). This script only runs agents and records metadata.
#
# Usage:
#   bash run.sh                                  # full sweep with defaults below
#   REPS=1 AGENTS=claude TASKS=trim-log bash run.sh   # quick smoke test
#   DRY_RUN=1 bash run.sh                         # print commands, run nothing
set -u

# ---- config (override via env) ---------------------------------------------
CLAUDE_MODEL="${CLAUDE_MODEL:-claude-sonnet-4-6}"
CODEX_MODEL="${CODEX_MODEL:-}"   # empty = codex default (required for ChatGPT-account auth)
CURSOR_MODEL="${CURSOR_MODEL:-composer-2.5}"

REPS="${REPS:-3}"
AGENTS="${AGENTS:-claude codex cursor}"
TASKS="${TASKS:-trim-log extract-json summarize grep-answer}"
CONDITIONS="${CONDITIONS:-without with}"
DRY_RUN="${DRY_RUN:-0}"
# ----------------------------------------------------------------------------

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
RUNS="$HERE/runs"
mkdir -p "$RUNS"
MANIFEST="$RUNS/manifest.jsonl"

now_ms() { python3 -c 'import time;print(int(time.time()*1000))'; }
jstr()   { python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$1"; }

run_one() {
  local agent="$1" task="$2" cond="$3" rep="$4"
  local id="${task}__${agent}__${cond}__r${rep}"
  local raw="$RUNS/${id}.out"
  local prompt; prompt="$(cat "$HERE/tasks/$task/prompt.txt")"

  # isolated working copy of the fixture (no prompt.txt / verify.sh leaked in)
  local wd; wd="$(mktemp -d)"
  cp -R "$HERE/tasks/$task/." "$wd/"
  rm -f "$wd/prompt.txt" "$wd/verify.sh"
  if [ "$cond" = "with" ]; then
    cp "$ROOT/CLAUDE.md" "$ROOT/AGENTS.md" "$wd/" 2>/dev/null
    mkdir -p "$wd/.cursor/rules"
    cp "$ROOT/.cursor/rules/token-economy.mdc" "$wd/.cursor/rules/" 2>/dev/null
  fi

  local cmd model
  case "$agent" in
    claude) model="$CLAUDE_MODEL"
            cmd=(claude -p --output-format json --model "$CLAUDE_MODEL"
                 --permission-mode bypassPermissions "$prompt") ;;
    codex)  model="${CODEX_MODEL:-default}"
            cmd=(codex exec --json --skip-git-repo-check)
            [ -n "$CODEX_MODEL" ] && cmd+=(-m "$CODEX_MODEL")
            cmd+=("$prompt") ;;
    cursor) model="$CURSOR_MODEL"
            cmd=(cursor-agent -p --output-format json --model "$CURSOR_MODEL"
                 --force --trust "$prompt") ;;
    *) echo "unknown agent: $agent" >&2; rm -rf "$wd"; return 1 ;;
  esac

  if [ "$DRY_RUN" = "1" ]; then
    echo "[dry] ($cond) cd $wd && ${cmd[*]}"
    rm -rf "$wd"; return 0
  fi

  echo ">> $id"
  local t0 t1 ec
  t0="$(now_ms)"
  ( cd "$wd" && "${cmd[@]}" ) >"$raw" 2>"$raw.err"
  ec=$?
  t1="$(now_ms)"

  # best-effort verify against raw stdout
  local success="null"
  if [ -f "$HERE/tasks/$task/verify.sh" ]; then
    if bash "$HERE/tasks/$task/verify.sh" "$raw" >/dev/null 2>&1; then
      success="true"; else success="false"; fi
  fi

  printf '{"id":%s,"task":%s,"agent":%s,"condition":%s,"rep":%d,"model":%s,"exit_code":%d,"wall_ms":%d,"success":%s,"raw":%s}\n' \
    "$(jstr "$id")" "$(jstr "$task")" "$(jstr "$agent")" "$(jstr "$cond")" \
    "$rep" "$(jstr "$model")" \
    "$ec" "$((t1 - t0))" "$success" "$(jstr "runs/${id}.out")" >>"$MANIFEST"

  rm -rf "$wd"
}

echo "models: claude=$CLAUDE_MODEL codex=${CODEX_MODEL:-default} cursor=$CURSOR_MODEL | reps=$REPS"
for agent in $AGENTS; do
  for task in $TASKS; do
    for cond in $CONDITIONS; do
      for rep in $(seq 1 "$REPS"); do
        run_one "$agent" "$task" "$cond" "$rep"
      done
    done
  done
done
echo "done -> $MANIFEST"
echo "next: python3 analyze.py"
