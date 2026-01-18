#!/usr/bin/env bash
# 02-customers-crud.sh
# Tests CRUD endpoints for /api/customers

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
SERVICE_DIR="$ROOT_DIR/backend/microservices/events_grasp_service"
SCRIPTS_DIR="$ROOT_DIR/scripts/backend/microservices/events_grasp_service"
LOG_DIR="$ROOT_DIR/runtime_data/logs"
mkdir -p "$LOG_DIR"
SERVER_LOG="$LOG_DIR/events_grasp_service.log"
PID_FILE="/tmp/events_grasp_service.pid"

VENV_PY="${VENV_PY:-$HOME/runtime_data/python_venvs/LLM-FineTuning-Solutions/bin/python3}"
CURL_BIN="${CURL_BIN:-$(command -v curl || true)}"
JQ_BIN="$(command -v jq || true)"
PY_BIN="${PY_BIN:-$(command -v python3 || true)}"

OUT_CUSTOMER_FILE="/tmp/eg_customer_id"

if [[ -z "$CURL_BIN" ]]; then
  echo "curl is required but not found" >&2
  exit 1
fi

is_server_up() { $CURL_BIN -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/ || true; }

start_server() {
  echo "Server not reachable; starting service..."
  if [[ ! -x "$VENV_PY" ]]; then
    echo "Python at $VENV_PY not found or not executable. Please set VENV_PY." >&2
    exit 1
  fi
  pushd "$SERVICE_DIR" > /dev/null
  nohup "$VENV_PY" run.py > "$SERVER_LOG" 2>&1 &
  echo $! > "$PID_FILE"
  popd > /dev/null
  echo "Started service (pid=$(cat $PID_FILE)), waiting..."
  for i in {1..30}; do
    status=$(is_server_up) || status=000
    if [[ "$status" == "200" ]]; then
      echo "Server ready"
      return 0
    fi
    sleep 1
  done
  echo "Server did not become ready" >&2
  return 1
}

code=$(is_server_up) || code=000
if [[ "$code" != "200" ]]; then
  start_server
fi

FAILED=0

# If customer id file exists, use it, otherwise create a new customer via signup
if [[ -f "$OUT_CUSTOMER_FILE" && -s "$OUT_CUSTOMER_FILE" ]]; then
  CUST_ID=$(cat "$OUT_CUSTOMER_FILE")
  echo "Using existing customer_id from $OUT_CUSTOMER_FILE: $CUST_ID"
else
  echo "No existing customer id found, creating via signup script"
  bash "$SCRIPTS_DIR/01-signup-auth.sh"
  if [[ -f "$OUT_CUSTOMER_FILE" && -s "$OUT_CUSTOMER_FILE" ]]; then
    CUST_ID=$(cat "$OUT_CUSTOMER_FILE")
  else
    echo "Failed to obtain customer id from signup"; exit 2
  fi
fi

# GET customer
out=$(curl -sS http://127.0.0.1:5000/api/customers/${CUST_ID}) || { echo "Get customer failed"; FAILED=$((FAILED+1)); }
if echo "$out" | grep -q "@example.com"; then
  echo "Get OK"
else
  echo "Get failed: $out"; FAILED=$((FAILED+1));
fi

# UPDATE customer
out=$(curl -sS -X PUT http://127.0.0.1:5000/api/customers/${CUST_ID} -H "Content-Type: application/json" -d "{\"first_name\":\"Updated\"}") || { echo "Update failed"; FAILED=$((FAILED+1)); }
if echo "$out" | grep -q 'success'; then
  echo "Update OK"
else
  echo "Update may have failed: $out"; FAILED=$((FAILED+1));
fi

# LIST customers
out=$(curl -sS http://127.0.0.1:5000/api/customers/) || { echo "List failed"; FAILED=$((FAILED+1)); }
if echo "$out" | grep -q "@example.com"; then
  echo "List OK"
else
  echo "List failed: $out"; FAILED=$((FAILED+1));
fi

# DELETE (cleanup)
out=$(curl -sS -X DELETE http://127.0.0.1:5000/api/customers/${CUST_ID}) || { echo "Delete failed"; FAILED=$((FAILED+1)); }
if echo "$out" | grep -q 'deleted'; then
  echo "Delete OK"
  rm -f "$OUT_CUSTOMER_FILE" || true
else
  echo "Delete may have failed: $out"; FAILED=$((FAILED+1));
fi

if [[ "$FAILED" -eq 0 ]]; then
  echo "\nALL CUSTOMERS CRUD TESTS PASSED"
  exit 0
else
  echo "\nSOME CUSTOMER TESTS FAILED: $FAILED failures"
  exit 2
fi
