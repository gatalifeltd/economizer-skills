#!/usr/bin/env bash
# Heavy multi-turn benchmark: one persistent session of N turns over a large
# (~120k-token) codebase fixture, run WITH and WITHOUT the policy files.
#
# The point: in a long session every turn resends the prior transcript, so any
# bloat an agent adds early (fat file dumps, verbose answers) is paid for again
# on every later turn. The economy rules suppress that bloat — savings compound
# with session length. We sum tokens across all turns of the session.
#
# Usage:
#   bash run_heavy.sh
#   REPS=1 AGENTS=codex TURNS=4 bash run_heavy.sh        # quick validation
#   DRY_RUN=1 bash run_heavy.sh
set -u

CODEX_MODEL="${CODEX_MODEL:-gpt-5.5}"
CURSOR_MODEL="${CURSOR_MODEL:-composer-2.5}"
OPUS_MODEL="${OPUS_MODEL:-claude-opus-4-8-high}"        # Claude via Cursor backend
SONNET_MODEL="${SONNET_MODEL:-claude-4.6-sonnet-medium}"

REPS="${REPS:-2}"
AGENTS="${AGENTS:-codex cursor}"          # add: opus sonnet  (Claude via cursor)
CONDITIONS="${CONDITIONS:-without with}"
TURNS="${TURNS:-0}"                        # 0 = all lines in session.txt
DRY_RUN="${DRY_RUN:-0}"

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
FIX="$HERE/tasks_heavy/codebase"
SESSION="$HERE/tasks_heavy/session.txt"
RUNS="$HERE/runs/heavy"
mkdir -p "$RUNS"
MANIFEST="$RUNS/manifest.jsonl"

now_ms() { python3 -c 'import time;print(int(time.time()*1000))'; }
jstr()   { python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$1"; }

PROMPTS=()
while IFS= read -r _line || [ -n "$_line" ]; do
  [ -n "$_line" ] && PROMPTS+=("$_line")
done < "$SESSION"
[ "$TURNS" -gt 0 ] && PROMPTS=("${PROMPTS[@]:0:$TURNS}")
NTURNS=${#PROMPTS[@]}

run_session() {
  local agent="$1" cond="$2" rep="$3"
  local id="heavy__${agent}__${cond}__r${rep}"
  local wd; wd="$(mktemp -d)"
  cp -R "$FIX/." "$wd/"
  if [ "$cond" = "with" ]; then
    cp "$ROOT/CLAUDE.md" "$ROOT/AGENTS.md" "$wd/" 2>/dev/null
    mkdir -p "$wd/.cursor/rules"; cp "$ROOT/.cursor/rules/token-economy.mdc" "$wd/.cursor/rules/" 2>/dev/null
  fi

  local model raws=() sid="" t0 t1
  case "$agent" in
    codex)  model="$CODEX_MODEL" ;;
    cursor) model="$CURSOR_MODEL" ;;
    opus)   model="$OPUS_MODEL" ;;
    sonnet) model="$SONNET_MODEL" ;;
    *) echo "unknown agent $agent" >&2; rm -rf "$wd"; return 1 ;;
  esac

  echo ">> $id ($NTURNS turns, model=$model)"
  t0="$(now_ms)"
  local k=0
  for prompt in "${PROMPTS[@]}"; do
    k=$((k+1))
    local raw; raw="$RUNS/${id}__t$(printf '%02d' "$k").out"
    raws+=("runs/heavy/$(basename "$raw")")
    if [ "$DRY_RUN" = "1" ]; then echo "  [dry] turn $k ($cond/$agent) sid=$sid"; continue; fi

    case "$agent" in
      codex)
        if [ "$k" -eq 1 ]; then
          ( cd "$wd" && codex exec --json --skip-git-repo-check -m "$model" "$prompt" ) >"$raw" 2>/dev/null
          sid="$(python3 -c 'import json,sys;[print(json.loads(l).get("thread_id","")) for l in open(sys.argv[1]) if "thread_id" in l]' "$raw" | head -1)"
        else
          ( cd "$wd" && codex exec resume "$sid" --json --skip-git-repo-check "$prompt" ) >"$raw" 2>/dev/null
        fi ;;
      *)  # cursor-family (cursor/opus/sonnet) all via cursor-agent
        if [ "$k" -eq 1 ]; then
          ( cd "$wd" && cursor-agent -p --output-format json --force --trust --model "$model" "$prompt" ) >"$raw" 2>/dev/null
          sid="$(python3 -c 'import json,sys;print(json.loads(open(sys.argv[1]).read(),strict=False).get("session_id",""))' "$raw" 2>/dev/null)"
        else
          ( cd "$wd" && cursor-agent -p --output-format json --resume "$sid" --force --trust --model "$model" "$prompt" ) >"$raw" 2>/dev/null
        fi ;;
    esac
  done
  t1="$(now_ms)"

  [ "$DRY_RUN" = "1" ] && { rm -rf "$wd"; return 0; }
  local raws_json; raws_json="$(printf '%s\n' "${raws[@]}" | python3 -c 'import json,sys;print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"
  printf '{"id":%s,"agent":%s,"condition":%s,"rep":%d,"model":%s,"turns":%d,"wall_ms":%d,"session_id":%s,"raws":%s}\n' \
    "$(jstr "$id")" "$(jstr "$agent")" "$(jstr "$cond")" "$rep" "$(jstr "$model")" \
    "$NTURNS" "$((t1-t0))" "$(jstr "$sid")" "$raws_json" >>"$MANIFEST"
  rm -rf "$wd"
}

echo "heavy: agents=[$AGENTS] reps=$REPS turns=$NTURNS"
for agent in $AGENTS; do
  for cond in $CONDITIONS; do
    for rep in $(seq 1 "$REPS"); do
      run_session "$agent" "$cond" "$rep"
    done
  done
done
echo "done -> $MANIFEST ; next: python3 analyze_heavy.py"
