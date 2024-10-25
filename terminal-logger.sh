# Create terminal-logger.sh
echo '#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set up log directory using project structure
LOG_DIR="$SCRIPT_DIR/data/output/logs"
mkdir -p "$LOG_DIR"

# Create a new log file with timestamp
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
HOSTNAME=$(hostname)
LOG_FILE="$LOG_DIR/terminal_${HOSTNAME}_${TIMESTAMP}.log"

# Function to log with timestamp
log_with_timestamp() {
    while IFS= read -r line; do
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] $line" | tee -a "$LOG_FILE"
    done
}

echo "Starting terminal logging to: $LOG_FILE"
echo "Terminal session started on $HOSTNAME at $(date)" > "$LOG_FILE"

# Start logging
script -f -q "$LOG_FILE" | log_with_timestamp
' > terminal-logger.sh

# Make it executable
chmod +x terminal-logger.sh