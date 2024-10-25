#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_DIR="$SCRIPT_DIR/data/output/logs"

# Keep only last 7 days of logs
find "$LOG_DIR" -name "terminal_*.log" -mtime +7 -delete

# Compress logs older than 1 day
find "$LOG_DIR" -name "terminal_*.log" -mtime +1 -exec gzip {} \;

