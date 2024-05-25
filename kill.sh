#!/bin/bash
PID=$(lsof -t -i:8040)
if [ -n "$PID" ]; then
    echo "Killing process on port 8040 with PID: $PID"
    kill -9 $PID
else
    echo "No process running on port 8040"
fi