#!/usr/bin/env bash
# 03-test-auth-signup-login.sh
# Tests signup, login, me, and logout endpoints for auth.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
SERVICE_DIR="$ROOT_DIR/backend/microservices/events_grasp_service"
LOG_DIR="$ROOT_DIR/runtime_data/logs"
mkdir -p "$LOG_DIR"
SERVER_LOG="$LOG_DIR/events_grasp_service.log"
PID_FILE="/tmp/events_grasp_service.pid"

VENV_PY="${VENV_PY:-$HOME/runtime_data/python_venvs/LLM-FineTuning-Solutions/bin/python3}"
CURL_BIN="${CURL_BIN:-$(command -v curl || true)}"
JQ_BIN="$(command -v jq || true)"
PY_BIN="${PY_BIN:-$(command -v python3 || true)}"

if [[ -z "$CURL_BIN" ]]; then
  echo "curl is required but not found" >&2
  exit 1
fi

parse_json() {
  local json="$1" filter="$2"
  if [[ -n "$JQ_BIN" && "$JQ_BIN" != "" ]]; then
    echo "$json" | $JQ_BIN -r "$filter"
  else
    $PY_BIN - <<PY
import sys,json
s=sys.stdin.read()
obj=json.loads(s or '{}')
parts='$filter'.strip('.').split('.') if '$filter' else []
# simple: support top-level key or .key
try:
    if not '$filter':
        print(json.dumps(obj))
    else:
        cur=obj
        for p in parts:
            cur=cur.get(p) if isinstance(cur, dict) else None
        if cur is None:
            print('')
        else:
            print(cur)
except Exception:
    print('')
PY
  fi
}

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

# Use timestamped email to avoid dup collisions
TS=$(date +%s)
EMAIL="test.user.${TS}@example.com"
PASSWORD='P@ssw0rd1'

# Signup
out=$(curl -sS -X POST http://127.0.0.1:5000/api/auth/signup -H "Content-Type: application/json" -d "{\"first_name\":\"Test\",\"last_name\":\"User\",\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}" ) || { echo "Signup request failed"; FAILED=$((FAILED+1)); }
if echo "$out" | grep -q 'customer_id'; then
  echo "Signup OK: $EMAIL"
else
  echo "Signup failed: $out"; FAILED=$((FAILED+1));
fi

# Login
out=$(curl -sS -X POST http://127.0.0.1:5000/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}" ) || { echo "Login request failed"; FAILED=$((FAILED+1)); }
TOKEN=$(echo "$out" | ( [[ -n "$JQ_BIN" && "$JQ_BIN" != "" ]] && $JQ_BIN -r '.token' || $PY_BIN -c "import sys,json; o=json.load(sys.stdin); print(o.get('token',''))" ))
if [[ -n "$TOKEN" && "$TOKEN" != "null" ]]; then
  echo "Login OK: token obtained"
else
  echo "Login failed: $out"; FAILED=$((FAILED+1));
fi

# Me
if [[ -n "$TOKEN" ]]; then
  out=$(curl -sS "http://127.0.0.1:5000/api/auth/me?token=${TOKEN}") || { echo "Me request failed"; FAILED=$((FAILED+1)); }
  if echo "$out" | grep -q "${EMAIL}"; then
    echo "Me OK"
  else
    echo "Me failed: $out"; FAILED=$((FAILED+1));
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
