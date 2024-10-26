#!/bin/bash

# Get timestamp in the required format
get_timestamp() {
    date +"[%Y-%m-%d %H:%M:%S]"
}

# Create logs directory if it doesn't exist
LOGS_DIR="data/output/logs"
mkdir -p "$LOGS_DIR"

# Generate log filename with timestamp
LOG_FILE="$LOGS_DIR/terminal_$(hostname)_$(date +%Y%m%d_%H%M%S).log"
CURRENT_LOG="$LOGS_DIR/terminal_$(hostname).log"

# Start logging
echo "Terminal session started on $(hostname) at $(date +'%a, %b %d, %Y %l:%M:%S %p')" | tee -a "$LOG_FILE" "$CURRENT_LOG"

# Function to log both command and output
log_command_and_output() {
    # Log the command with timestamp
    echo "$(get_timestamp) Command: $BASH_COMMAND" >> "$LOG_FILE"
    echo "$(get_timestamp) Command: $BASH_COMMAND" >> "$CURRENT_LOG"
    
    # Execute the command and capture its output
    output=$("$@" 2>&1)
    
    # If there's any output, log it with timestamp
    if [ ! -z "$output" ]; then
        while IFS= read -r line; do
            echo "$(get_timestamp) Output: $line" >> "$LOG_FILE"
            echo "$(get_timestamp) Output: $line" >> "$CURRENT_LOG"
        done <<< "$output"
    fi
    
    # Display the output to the terminal
    echo "$output"
}

# Set up trap to log all commands and their output
trap 'log_command_and_output "$BASH_COMMAND"' DEBUG

# Inform user that logging has started
echo "Logging enabled - all commands will be logged to $LOG_FILE"

# Keep the terminal session active with logging
exec script -q -f "$LOG_FILE" /dev/null
