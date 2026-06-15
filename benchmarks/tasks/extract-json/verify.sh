#!/usr/bin/env bash
# $1 = path to raw agent output. Check a couple of known id/email pairs appear.
out="$1"
grep -q "1001" "$out" && grep -q "ada@example.com" "$out" &&
grep -q "1042" "$out" && grep -q "grace@example.com" "$out"
