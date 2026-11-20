#!/bin/bash
# ing.sh <hash...>: ingest hashes in order of req/last_round.txt (all qids of the last emit)
A=/cursor/stores/user/grok-bot/agents/541d1ad4-458c-449f-a6ec-f1b5f02d3dfe/assets/
cd /workspace/gop-lobby-graph/full/x_all; mapfile -t Q < req/last_round.txt; args=(); i=0
for h in "$@"; do args+=("${Q[$i]}" "$A$h.txt"); i=$((i+1)); done
python3 bin/ingest.py "${args[@]}"
