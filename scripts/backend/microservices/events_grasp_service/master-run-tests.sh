#!/usr/bin/env bash
# master-run-tests.sh
# Master test runner for events_grasp_service numbered test scripts.
# Usage:
#   master-run-tests.sh [events|all|<script-number>|<script-filename>]
# Examples:
#   master-run-tests.sh events      -> runs signup (01), customers (02), then events (03)
#   master-run-tests.sh all         -> runs preferred sequence then any other numbered scripts
#   master-run-tests.sh 01          -> runs 01-signup-auth.sh
#   master-run-tests.sh 01-signup-auth.sh -> runs that file

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Master test runner started at $(date)"

run_script() {
  local script_path="$1"
  echo "\n--- Running: $script_path ---"
  if [[ ! -x "$script_path" ]]; then
    echo "Making $script_path executable"
    chmod +x "$script_path" || true
  fi
  "$script_path"
  local rc=$?
  if [[ $rc -ne 0 ]]; then
    echo "Script failed with exit code $rc: $script_path"
  else
    echo "Script completed: $script_path"
  fi
  return $rc
}

failures=0

case "${1:-events}" in
  events)
    # Preferred execution order for an events-focused integration run:
    # 1) signup/auth tests (01)
    # 2) customers CRUD (02)
    # 3) events CRUD (03)
    run_script "$SCRIPTS_DIR/01-signup-auth.sh" || failures=$((failures+1))
    run_script "$SCRIPTS_DIR/02-customers-crud.sh" || failures=$((failures+1))
    run_script "$SCRIPTS_DIR/03-events-crud.sh" || failures=$((failures+1))
    ;;
  all)
    # Run preferred sequence first (so dependencies are prepared)
    preferred=("01-signup-auth.sh" "02-customers-crud.sh" "03-events-crud.sh")
    for p in "${preferred[@]}"; do
      f="$SCRIPTS_DIR/$p"
      if [[ -f "$f" ]]; then
        run_script "$f" || failures=$((failures+1))
      fi
    done

    # Then run any other numbered scripts in numeric order, skipping the stop script (99)
    for f in "$SCRIPTS_DIR"/[0-9][0-9]-*.sh; do
      [[ -e "$f" ]] || continue
      base="$(basename "$f")"
      # skip preferred ones and the stop script
      if [[ " ${preferred[*]} " == *" $base "* ]] || [[ "$base" == "99-stop-events-service.sh" ]]; then
        continue
      fi
      run_script "$f" || failures=$((failures+1))
    done
    ;;
  [0-9][0-9])
    # Map explicit two-digit to either new names or legacy names
    nn=$(printf "%02d" "$1")
    # prefer new naming pattern
    candidates=("$SCRIPTS_DIR/${nn}-*.sh" "$SCRIPTS_DIR/${nn}-*.sh" "$SCRIPTS_DIR/*${nn}*.sh")
    for m in "${candidates[@]}"; do
      for file in $m; do
        if [[ -f "$file" ]]; then
          run_script "$file" || failures=$((failures+1))
        fi
      done
    done
    ;;
  *.sh)
    if [[ -f "$SCRIPTS_DIR/$1" ]]; then
      run_script "$SCRIPTS_DIR/$1" || failures=$((failures+1))
    else
      echo "Script not found: $1"; exit 2
    fi
    ;;
  *)
    echo "Unknown option: $1" >&2
    echo "Usage: $0 [events|all|<NN>|<script-filename>]" >&2
    exit 2
    ;;
esac

if [[ $failures -eq 0 ]]; then
  echo "\nMASTER RUN: ALL TESTS PASSED"
  exit 0
else
  echo "\nMASTER RUN: Completed with $failures failed script(s)"
  exit 3
fi
