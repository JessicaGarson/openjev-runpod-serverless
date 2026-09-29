#!/usr/bin/env bash
set -euo pipefail
: "${RUNPOD_API_KEY:?Set RUNPOD_API_KEY}"
: "${ENDPOINT_ID:?Set ENDPOINT_ID}"
example_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
bash "$example_dir/wait-ready.sh"
curl --fail-with-body -sS --max-time 60 \
  "https://$ENDPOINT_ID.api.runpod.ai/v1/systemone" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary "@$example_dir/request.json" \
  -w '\n'
