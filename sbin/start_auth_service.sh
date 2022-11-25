#!/usr/bin/env bash
LOGS_DIR=logs
cd "$CODEBASE_DIR/authservice"
if [[ ! -e $LOGS_DIR ]] 
then
  mkdir "$LOGS_DIR"
fi
nohup python -u "./main/server.py" >> "${LOGS_DIR}/authservice.out" 2>&1 & echo $! > "${LOGS_DIR}/.authservice.pid"
pid=$(cat "${LOGS_DIR}/.authservice.pid")
echo "Started authservice with PID:${pid}"