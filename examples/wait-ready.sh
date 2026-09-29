#!/usr/bin/env bash
set -euo pipefail
: "${RUNPOD_API_KEY:?Set RUNPOD_API_KEY}"
: "${ENDPOINT_ID:?Set ENDPOINT_ID}"
deadline=$(( $(date +%s) + 1200 ))
while [ "$(date +%s)" -lt "$deadline" ]; do
  remaining=$(( deadline - $(date +%s) ))
  timeout=130
  if [ "$remaining" -lt "$timeout" ]; then timeout=$remaining; fi
  if [ "$timeout" -le 0 ]; then break; fi
  response=$(curl -sS --connect-timeout 10 --max-time "$timeout" -w '\n%{http_code}' \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    "https://$ENDPOINT_ID.api.runpod.ai/v1/version") || true
  code=${response##*$'\n'}
  body=${response%$'\n'*}
  if [ "$code" = 200 ]; then echo 'Worker ready.'; exit 0; fi
  case "$body" in
    *'not allowed for QB API'*) echo 'Use a Load balancer endpoint, not Queue.' >&2; exit 1 ;;
  esac
  case "$code" in
    401|403) echo "HTTP $code: check API key and endpoint permissions." >&2; exit 1 ;;
    400|404) echo "HTTP $code: check endpoint ID and configuration." >&2; exit 1 ;;
  esac
  echo "Not ready yet (HTTP $code): ${body:-(no response)}"
  sleep 10
done
echo 'Worker not ready within 20 minutes. Check worker logs.' >&2
exit 1
