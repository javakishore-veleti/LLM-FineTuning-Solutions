#!/usr/bin/env bash
# 01-signup-auth.sh
# Tests signup, login, me, and logout endpoints for auth and writes customer_id to /tmp/eg_customer_id

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

TS=$(date +%s)
EMAIL="test.user.${TS}@example.com"
PASSWORD='P@ssw0rd1'

# Helper to run curl and return body and status
curl_with_status() {
  # args: method url data
  local method="$1" url="$2" data="$3"
  if [[ "$method" == "GET" || -z "$data" ]]; then
    $CURL_BIN -sS -w "\n%{http_code}" -X "$method" "$url"
  else
    $CURL_BIN -sS -w "\n%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" "$url"
  fi
}

# Signup
resp_and_status=$(curl_with_status POST http://127.0.0.1:5000/api/auth/signup "{\"first_name\":\"Test\",\"last_name\":\"User\",\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}") || { echo "Signup request failed"; FAILED=$((FAILED+1)); }
status=$(echo "$resp_and_status" | tail -n1)
body=$(echo "$resp_and_status" | sed '$d')

if [[ "$status" != "200" && "$status" != "201" ]]; then
  echo "Signup HTTP status: $status" >&2
  echo "Response body:" >&2
  echo "$body" >&2
  echo "Check server log: $SERVER_LOG" >&2
  FAILED=$((FAILED+1))
else
  # parse customer_id safely
  if [[ -n "$body" ]]; then
    if [[ -n "$JQ_BIN" && "$JQ_BIN" != "" ]]; then
      CUSTOMER_ID=$(echo "$body" | $JQ_BIN -r '.customer_id' 2>/dev/null || true)
    else
      CUSTOMER_ID=$(echo "$body" | $PY_BIN -c 'import sys,json
s=sys.stdin.read().strip()
if not s: print("");
else:
 try:
  o=json.loads(s)
  print(o.get("customer_id", ""))
 except Exception:
  print("")')
    fi
  else
    CUSTOMER_ID=""
  fi

  if [[ -n "$CUSTOMER_ID" && "$CUSTOMER_ID" != "null" ]]; then
    echo "Signup OK: ${EMAIL} (customer_id=${CUSTOMER_ID})"
    echo "$CUSTOMER_ID" > "$OUT_CUSTOMER_FILE"
  else
    echo "Signup returned no customer_id; body:" >&2
    echo "$body" >&2
    FAILED=$((FAILED+1))
  fi
fi

# Login
resp_and_status=$(curl_with_status POST http://127.0.0.1:5000/api/auth/login "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}") || { echo "Login request failed"; FAILED=$((FAILED+1)); }
status=$(echo "$resp_and_status" | tail -n1)
body=$(echo "$resp_and_status" | sed '$d')

if [[ "$status" != "200" ]]; then
  echo "Login HTTP status: $status" >&2
  echo "$body" >&2
  FAILED=$((FAILED+1))
else
  if [[ -n "$body" ]]; then
    if [[ -n "$JQ_BIN" && "$JQ_BIN" != "" ]]; then
      TOKEN=$(echo "$body" | $JQ_BIN -r '.token' 2>/dev/null || true)
    else
      TOKEN=$(echo "$body" | $PY_BIN -c 'import sys,json
s=sys.stdin.read().strip()
if not s: print("")
else:
 try:
  o=json.loads(s)
  print(o.get("token",""))
 except Exception:
  print("")')
    fi
  else
    TOKEN=""
  fi

  if [[ -n "$TOKEN" && "$TOKEN" != "null" ]]; then
    echo "Login OK: token obtained"
  else
    echo "Login failed, body:" >&2
    echo "$body" >&2
    FAILED=$((FAILED+1))
  fi
fi

# Me
if [[ -n "$TOKEN" ]]; then
  me_out=$(curl -sS -X GET "http://127.0.0.1:5000/api/auth/me?token=${TOKEN}" ) || { echo "Me request failed"; FAILED=$((FAILED+1)); }
  if echo "$me_out" | grep -q "${EMAIL}"; then
    echo "Me OK"
  else
    echo "Me failed: $me_out"; FAILED=$((FAILED+1));
  fi
else
  echo "Skipping me check because no token"; FAILED=$((FAILED+1));
fi

# Logout
if [[ -n "$TOKEN" ]]; then
  out=$(curl -sS -X POST http://127.0.0.1:5000/api/auth/logout -H "Content-Type: application/json" -d "{\"token\":\"${TOKEN}\"}") || { echo "Logout request failed"; FAILED=$((FAILED+1)); }
  if echo "$out" | grep -q -e 'ok' -e 'true' ; then
    echo "Logout OK"
  else
    echo "Logout may have failed: $out"; FAILED=$((FAILED+1));
  fi
fi

if [[ "$FAILED" -eq 0 ]]; then
  echo "\nALL AUTH TESTS PASSED"
  exit 0
else
  echo "\nSOME AUTH TESTS FAILED: $FAILED failures"
  exit 2
fi
