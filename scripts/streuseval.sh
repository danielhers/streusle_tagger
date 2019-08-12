#!/usr/bin/env bash

REF="$1"
shift
for PRED in "$@"; do
    python scripts/streusle_set_lextag.py "$REF" "$PRED" > "$(basename "$PRED" .jsonl)".autoid.json
done
python -m streuseval "$REF" *.autoid.json
