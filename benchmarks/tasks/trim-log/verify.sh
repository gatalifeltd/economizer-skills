#!/usr/bin/env bash
# Exit 0 if the agent's stdout (passed as $1 = path to raw output) contains the 3
# expected ERROR lines. Best-effort: checks the known last-3 error markers exist.
out="$1"
grep -q "ERROR db timeout on shard 7" "$out" &&
grep -q "ERROR cache eviction storm" "$out" &&
grep -q "ERROR payment webhook 503" "$out"
