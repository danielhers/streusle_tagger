#!/usr/bin/env bash

REF="$1"

shift
for PRED in "$@"; do
    PREFIX="$(basename "$PRED" .jsonl)".
    python scripts/streusle_set_lextag.py "$REF" "$PRED" > "$PREFIX"json
    python -m json2conllulex "$PREFIX"json > "$PREFIX"conllulex
    python -m conllulex2UDlextag "$PREFIX"conllulex > "$PREFIX"UDlextag
    python -m UDlextag2json "$PREFIX"UDlextag > "$PREFIX"autoid.json
done
python -m streuseval "$REF" *.autoid.json
