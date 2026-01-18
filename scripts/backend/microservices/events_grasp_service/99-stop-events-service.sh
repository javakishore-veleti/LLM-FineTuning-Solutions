#!/usr/bin/env bash
# 99-stop-events-service.sh
# Stop the events_grasp_service server started by the test script (if pid file exists)

PID_FILE="/tmp/events_grasp_service.pid"
if [[ -f "$PID_FILE" ]]; then
  pid=$(cat "$PID_FILE")
  echo "Stopping process $pid"
  kill "$pid" || true
  rm -f "$PID_FILE"
  echo "Stopped"
else
  echo "No pid file found at $PID_FILE"
fi
