#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set up log directory using project structure
LOG_DIR="$SCRIPT_DIR/data/output/logs"
mkdir -p "$LOG_DIR"

# Set max log size (in bytes) - 10MB
MAX_LOG_SIZE=$((10 * 1024 * 1024))

# Use a consistent log file name for the current host
HOSTNAME=$(hostname)
LOG_FILE="$LOG_DIR/terminal_${HOSTNAME}.log"

# Function to check log size and rotate if needed
check_log_size() {
    if [ -f "$LOG_FILE" ]; then
        local size=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null)
        if [ "$size" -gt "$MAX_LOG_SIZE" ]; then
            local timestamp=$(date "+%Y%m%d_%H%M%S")
            mv "$LOG_FILE" "${LOG_FILE%.log}_${timestamp}.log"
            gzip "${LOG_FILE%.log}_${timestamp}.log"
            echo "Log file rotated due to size ($size bytes)" > "$LOG_FILE"
        fi
    fi
}

# Create log file if it doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    echo "Terminal session started on $HOSTNAME at $(date)" > "$LOG_FILE"
else
    echo "Terminal session resumed on $HOSTNAME at $(date)" >> "$LOG_FILE"
fi

# Function to log commands and their output
log_command() {
    # Check and rotate log if needed
    check_log_size
    
    # Get the command from history
    local cmd=$(history 1 | sed 's/^\s*[0-9]*\s*//')
    
    # Don't log the log_command function itself
    if [[ "$cmd" != "log_command"* ]]; then
        # Log the command
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] Command: $cmd" | tee -a "$LOG_FILE"
        
        # Execute the command and capture its output
        eval "$cmd" 2>&1 | while read -r line; do
            echo "[$(date "+%Y-%m-%d %H:%M:%S")] Output: $line" | tee -a "$LOG_FILE"
        done
    fi
}

# Set up trap to log commands
trap 'log_command' DEBUG

echo "Logging enabled - all commands will be logged to $LOG_FILE"