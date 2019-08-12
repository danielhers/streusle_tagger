#!/usr/bin/env bash

REF=$1
shift
for d in $*; do
    IN=$d/predictions.txt
    OUT=$d/`basename $REF .json`.autoid.json
    [ -f $IN ] && python scripts/streusle_set_lextag.py $REF $IN > $OUT && echo $OUT
done
python -m streuseval streusle.ud_test.json models/*/streusle.ud_test.autoid.json
