#!/usr/bin/env bash
# 3-arm single-turn benchmark on output-heavy tasks:
#   without  — no policy file
#   full     — the full 12-rule policy (repo root CLAUDE.md/AGENTS.md/.cursor)
#   min      — the 3-rule minimal policy (benchmarks/policy_min/)
#
# Output-heavy tasks isolate the only channel the model controls: output length.
# 'full' should cut output but carry ~700 tokens of weight; 'min' cuts output for
# ~75 tokens of weight -> the net should be best for 'min'.
#
# Usage: bash run_min.sh ; REPS=1 AGENTS=codex TASKS=explain-ledger bash run_min.sh
set -u

CODEX_MODEL="${CODEX_MODEL:-gpt-5.5}"
CURSOR_MODEL="${CURSOR_MODEL:-composer-2.5}"
OPUS_MODEL="${OPUS_MODEL:-claude-opus-4-8-high}"
SONNET_MODEL="${SONNET_MODEL:-claude-4.6-sonnet-medium}"

REPS="${REPS:-3}"
AGENTS="${AGENTS:-codex cursor}"
TASKS="${TASKS:-explain-ledger review-retry describe-arch summarize-doc}"
CONDITIONS="${CONDITIONS:-without full min}"
DRY_RUN="${DRY_RUN:-0}"

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
RUNS="$HERE/runs/min"; mkdir -p "$RUNS"
MANIFEST="$RUNS/manifest.jsonl"

now_ms() { python3 -c 'import time;print(int(time.time()*1000))'; }
jstr()   { python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$1"; }

inject() {  # $1=condition $2=workdir
  case "$1" in
    full) cp "$HERE/policy_full/CLAUDE.md" "$HERE/policy_full/AGENTS.md" "$2/" 2>/dev/null
          mkdir -p "$2/.cursor/rules"; cp "$HERE/policy_full/.cursor/rules/token-economy.mdc" "$2/.cursor/rules/" 2>/dev/null ;;
    min)  cp "$HERE/policy_min/CLAUDE.md" "$HERE/policy_min/AGENTS.md" "$2/" 2>/dev/null
          mkdir -p "$2/.cursor/rules"; cp "$HERE/policy_min/.cursor/rules/token-economy.mdc" "$2/.cursor/rules/" 2>/dev/null ;;
  esac
}

run_one() {
  local agent="$1" task="$2" cond="$3" rep="$4"
  local id="${task}__${agent}__${cond}__r${rep}"
  local raw="$RUNS/${id}.out"
  local prompt; prompt="$(cat "$HERE/tasks_output/$task/prompt.txt")"
  local wd; wd="$(mktemp -d)"
  cp -R "$HERE/tasks_output/$task/." "$wd/"; rm -f "$wd/prompt.txt"
  inject "$cond" "$wd"

  local model cmd
  case "$agent" in
    codex)  model="$CODEX_MODEL"; cmd=(codex exec --json --skip-git-repo-check -m "$CODEX_MODEL" "$prompt") ;;
    cursor) model="$CURSOR_MODEL"; cmd=(cursor-agent -p --output-format json --force --trust --model "$CURSOR_MODEL" "$prompt") ;;
    opus)   model="$OPUS_MODEL"; cmd=(cursor-agent -p --output-format json --force --trust --model "$OPUS_MODEL" "$prompt") ;;
    sonnet) model="$SONNET_MODEL"; cmd=(cursor-agent -p --output-format json --force --trust --model "$SONNET_MODEL" "$prompt") ;;
    *) echo "unknown agent $agent" >&2; rm -rf "$wd"; return 1 ;;
  esac

  if [ "$DRY_RUN" = "1" ]; then echo "[dry] $id"; rm -rf "$wd"; return 0; fi
  echo ">> $id"
  local t0 t1 ec; t0="$(now_ms)"
  ( cd "$wd" && "${cmd[@]}" ) >"$raw" 2>/dev/null; ec=$?
  t1="$(now_ms)"
  printf '{"id":%s,"task":%s,"agent":%s,"condition":%s,"rep":%d,"model":%s,"exit_code":%d,"wall_ms":%d,"raw":%s}\n' \
    "$(jstr "$id")" "$(jstr "$task")" "$(jstr "$agent")" "$(jstr "$cond")" "$rep" "$(jstr "$model")" \
    "$ec" "$((t1-t0))" "$(jstr "runs/min/${id}.out")" >>"$MANIFEST"
  rm -rf "$wd"
}

echo "min: agents=[$AGENTS] tasks=[$TASKS] conditions=[$CONDITIONS] reps=$REPS"
for agent in $AGENTS; do for task in $TASKS; do for cond in $CONDITIONS; do
  for rep in $(seq 1 "$REPS"); do run_one "$agent" "$task" "$cond" "$rep"; done
done; done; done
echo "done -> $MANIFEST ; next: python3 analyze_min.py"
