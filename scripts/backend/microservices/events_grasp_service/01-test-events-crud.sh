#!/usr/bin/env bash
# 01-test-events-crud.sh
# Run a full CRUD smoke test against the events API (create, list, get, update, delete)
# - Starts the backend service if not reachable
# - Uses jq if available; otherwise uses python for JSON parsing

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)" # repo root/scripts/backend/microservices -> ../../../
SERVICE_DIR="$ROOT_DIR/backend/microservices/events_grasp_service"
LOG_DIR="$ROOT_DIR/runtime_data/logs"
mkdir -p "$LOG_DIR"
SERVER_LOG="$LOG_DIR/events_grasp_service.log"
PID_FILE="/tmp/events_grasp_service.pid"

# Configurable python binary (venv)
VENV_PY="${VENV_PY:-$HOME/runtime_data/python_venvs/LLM-FineTuning-Solutions/bin/python3}"
CURL_BIN="${CURL_BIN:-$(command -v curl || true)}"
JQ_BIN="$(command -v jq || true)"
PY_BIN="$(command -v python3 || true)"

if [[ -z "$CURL_BIN" ]]; then
  echo "curl is required but not found in PATH" >&2
  exit 1
fi

parse_json() {
  # parse_json <json_string> <jq_filter>
  local json="$1" filter="$2"
  if [[ -n "$JQ_BIN" ]]; then
    echo "$json" | $JQ_BIN -r "$filter"
  else
    # fallback to python
    $PY_BIN - <<PY -c "$json" "$filter"
import sys, json
s = sys.stdin.read()
obj = json.loads(s)
# filter coming from argv[1]
f = sys.argv[1]
# very simple: support .a.b and top-level keys
parts = f.strip('.').split('.') if f else []
cur = obj
try:
    for p in parts:
        if p == '':
            continue
        cur = cur.get(p) if isinstance(cur, dict) else None
    if cur is None:
        print('', end='')
    elif isinstance(cur, bool):
        print('true' if cur else 'false')
    else:
        print(cur)
except Exception:
    print('', end='')
PY
  fi
}

is_server_up() {
  $CURL_BIN -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/ || true
}

start_server() {
  echo "Server not reachable; starting service..."
  if [[ ! -x "$VENV_PY" ]]; then
    echo "Python at $VENV_PY not found or not executable. Please create the venv or set VENV_PY env var." >&2
    exit 1
  fi
  pushd "$SERVICE_DIR" > /dev/null
  nohup "$VENV_PY" run.py > "$SERVER_LOG" 2>&1 &
  local pid=$!
  echo $pid > "$PID_FILE"
  popd > /dev/null
  echo "Started service (pid=$pid), waiting for it to be ready..."
  # wait for HTTP 200 on / (timeout 30s)
  for i in {1..30}; do
    status=$(is_server_up) || status=000
    if [[ "$status" == "200" ]]; then
      echo "Server ready"
      return 0
    fi
    sleep 1
  done
  echo "Server did not become ready in time; check $SERVER_LOG" >&2
  return 1
}

# Ensure server
code=$(is_server_up) || code=000
if [[ "$code" != "200" ]]; then
  start_server
fi

# Helper to run curl and capture output
run_curl() {
  local method="$1" url="$2" data="$3"
  if [[ "$method" == "GET" || -z "$data" ]]; then
    $CURL_BIN -sS -X "$method" "$url"
  else
    $CURL_BIN -sS -X "$method" -H "Content-Type: application/json" -d "$data" "$url"
  fi
}

# Test sequence
echo "Running Events CRUD tests against http://127.0.0.1:5000"
FAILED=0

# 1) Create
payload='{"event_name":"Test Script Event","source_url":"https://example.com/test-event","event_description":"created by test script"}'
out=$(run_curl POST http://127.0.0.1:5000/api/events/ "$payload") || { echo "Create request failed"; FAILED=$((FAILED+1)); }
if [[ -z "$out" ]]; then
  echo "Empty response from create"; FAILED=$((FAILED+1));
else
  event_id=$(echo "$out" | ( [[ -n "$JQ_BIN" ]] && $JQ_BIN -r '.event.event_id // .event_id // .event?.event_id' || $PY_BIN -c "import sys,json; o=json.load(sys.stdin); print(o.get('event',{}).get('event_id') or o.get('event_id') or '')" ))
  if [[ -z "$event_id" || "$event_id" == "null" ]]; then
    echo "Create did not return event id: $out"; FAILED=$((FAILED+1));
  else
    echo "Create OK - event_id=$event_id"
  fi
fi

# 2) List
out=$(run_curl GET http://127.0.0.1:5000/api/events/ "") || { echo "List request failed"; FAILED=$((FAILED+1)); }
if [[ -z "$out" ]]; then
  echo "Empty response from list"; FAILED=$((FAILED+1));
else
  # check event name present
  if echo "$out" | grep -q "Test Script Event"; then
    echo "List OK"
  else
    echo "List did not include created event"; FAILED=$((FAILED+1));
  fi
fi

# 3) Get by id
out=$(run_curl GET http://127.0.0.1:5000/api/events/$event_id "") || { echo "Get request failed"; FAILED=$((FAILED+1)); }
if echo "$out" | grep -q "Test Script Event"; then
  echo "Get OK"
else
  echo "Get failed or wrong payload: $out"; FAILED=$((FAILED+1));
fi

# 4) Update
payload='{"event_name":"Test Script Event Updated","source_url":"https://example.com/updated"}'
out=$(run_curl PUT http://127.0.0.1:5000/api/events/$event_id "$payload") || { echo "Update request failed"; FAILED=$((FAILED+1)); }
if echo "$out" | grep -q "Test Script Event Updated"; then
  echo "Update OK"
else
  echo "Update did not reflect: $out"; FAILED=$((FAILED+1));
fi

# 5) Delete
out=$(run_curl DELETE http://127.0.0.1:5000/api/events/$event_id "") || { echo "Delete request failed"; FAILED=$((FAILED+1)); }
# try to detect deletion success
if echo "$out" | grep -q "deleted\": true" || echo "$out" | grep -q "success\": true" || echo "$out" | grep -q "deleted"; then
  echo "Delete OK"
else
  echo "Delete may have failed: $out"; FAILED=$((FAILED+1));
fi

# Summary
if [[ "$FAILED" -eq 0 ]]; then
  echo "\nALL EVENTS CRUD TESTS PASSED"
  exit 0
else
  echo "\nSOME TESTS FAILED: $FAILED failures"
  exit 2
fi
