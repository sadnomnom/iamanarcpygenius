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
CURRENT_LOG="${LOGS_DIR}/terminal_${HOSTNAME}.log"

# Start logging
echo "Terminal session started on ${HOSTNAME} at $(date +'%a, %b %d, %Y %l:%M:%S %p')" | tee -a "$LOG_FILE"

# Function to log both command and output
log_command_and_output() {
    # Log the command with timestamp
    echo "$(get_timestamp) Command: $BASH_COMMAND" | tee -a "$LOG_FILE"
    
    # Execute the command and capture its output
    output=$("$@" 2>&1)
    
    # If there's any output, log it with timestamp
    if [ ! -z "$output" ]; then
        while IFS= read -r line; do
            echo "$(get_timestamp) Output: $line" | tee -a "$LOG_FILE"
        done <<< "$output"
    fi
    
    # Display the output to the terminal
    echo "$output"
}

# Set up trap to log all commands and their output
trap 'log_command_and_output "$BASH_COMMAND"' DEBUG

# Inform user that logging has started
echo "Logging enabled - all commands will be logged to ${LOG_FILE}"

# Keep the terminal session active with logging
exec script -qf "$LOG_FILE" /dev/null
