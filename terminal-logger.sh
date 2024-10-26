#!/bin/bash

# Get timestamp in the required format
get_timestamp() {
    date +"[%Y-%m-%d %H:%M:%S]"
}

# Create logs directory if it doesn't exist
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOGS_DIR="${SCRIPT_DIR}/data/output/logs"
mkdir -p "$LOGS_DIR"

# Generate log filename with hostname
HOSTNAME=$(hostname)
LOG_FILE="${LOGS_DIR}/terminal_${HOSTNAME}.log"

# Start logging
echo "Terminal session started on ${HOSTNAME} at $(date +'%a, %b %d, %Y %l:%M:%S %p')" > "$LOG_FILE"

# Function to log both command and output
log_command_and_output() {
    local cmd="$1"
    local timestamp=$(get_timestamp)
    
    # Log the command
    echo "${timestamp} Command: ${cmd}" | tee -a "$LOG_FILE"
    
    # Execute the command and capture its output
    output=$( eval "$cmd" 2>&1 )
    
    # Log each line of output with timestamp
    if [ ! -z "$output" ]; then
        while IFS= read -r line; do
            echo "${timestamp} Output: ${line}" | tee -a "$LOG_FILE"
        done <<< "$output"
    fi
}

# Set up trap to log commands
trap 'log_command_and_output "$BASH_COMMAND"' DEBUG

# Inform user that logging has started
echo "Logging enabled - all commands will be logged to ${LOG_FILE}"

# Keep terminal session active
if command -v script >/dev/null 2>&1; then
    # Use script command if available (Unix/Linux)
    script -qf "$LOG_FILE" /dev/null
else
    # Otherwise just keep the shell running (Windows)
    exec bash --login -i
fi
