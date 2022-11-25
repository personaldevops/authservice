#!/usr/bin/env bash
LOGS_DIR=logs
cd "$CODEBASE_DIR/authservice/"
if [[ -f "${LOGS_DIR}/.authservice.pid" ]] 
then
    pid=$(cat "${LOGS_DIR}/.authservice.pid")
    kill "${pid}"
fi
echo "Stopped authservice with PID:${pid}"
