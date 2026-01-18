#!/usr/bin/env bash
# master-run-tests.sh
# Master test runner for events_grasp_service numbered test scripts.
# Usage:
#   master-run-tests.sh [events|all|<script-number>|<script-filename>]
# Examples:
#   master-run-tests.sh events      -> runs 01-test-events-crud.sh
#   master-run-tests.sh all         -> runs all numbered tests (01,02,...)
#   master-run-tests.sh 01          -> runs 01-test-events-crud.sh
#   master-run-tests.sh 01-test-events-crud.sh -> runs that file

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
    run_script "$SCRIPTS_DIR/01-test-events-crud.sh" || failures=$((failures+1))
    ;;
  all)
    # run all numbered scripts except the stop script (99) which is for manual stop
    for f in "$SCRIPTS_DIR"/[0-9][0-9]-*.sh; do
      # skip if none
      [[ -e "$f" ]] || continue
      # skip stop script
      if [[ "$(basename "$f")" == "99-stop-events-service.sh" ]]; then
        continue
      fi
      run_script "$f" || failures=$((failures+1))
    done
    ;;
  [0-9][0-9])
    file="$SCRIPTS_DIR/$(printf "%02d" "$1")-*.sh"
    # find matching
    matches=( $SCRIPTS_DIR/${1}-*.sh $SCRIPTS_DIR/$(printf "%02d" "$1")-*.sh )
    for m in "${matches[@]}"; do
      if [[ -f "$m" ]]; then
        run_script "$m" || failures=$((failures+1))
      fi
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
