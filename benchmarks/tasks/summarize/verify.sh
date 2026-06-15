#!/usr/bin/env bash
# $1 = path to raw agent output. Pass if at most 6 bullet-ish lines were produced
# (allow a little slack for formatting) and the output is non-empty.
out="$1"
bullets=$(grep -cE '^\s*[-*•]|^\s*[0-9]+\.' "$out")
[ "$bullets" -ge 1 ] && [ "$bullets" -le 6 ]
