#!/usr/bin/env bash
# $1 = path to raw agent output. The definition lives in src/billing/ledger.py.
out="$1"
grep -q "ledger.py" "$out"
