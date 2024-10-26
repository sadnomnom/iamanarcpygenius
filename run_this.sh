#!/bin/bash

# Set environment variables
export PYTHONPATH="."
export ARCGIS_PYTHON_API_VERSION=3.0
export PYTHONUNBUFFERED=1  # Disable Python output buffering

# Default test values for debugging
TEST_SUBSTATION="EMILIE"  # Valid substation from config
TEST_YEAR="2024"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to handle errors and keep terminal open
handle_error() {
    echo -e "${RED}Error occurred: $1${NC}"
    echo "Press Enter to continue..."
    read
    exit 1
}

# Trap errors
trap 'handle_error "Script interrupted"' INT TERM

echo "Verifying environment setup..."

# Run verification with immediate output
python -u -m scripts.cli verify
VERIFY_STATUS=$?

if [ $VERIFY_STATUS -eq 0 ]; then
    echo -e "${GREEN}Verification successful!${NC}"
    
    # Run the main script with immediate output
    python -u -m scripts.cli generate-maps "$TEST_SUBSTATION" --year "$TEST_YEAR"
    MAP_STATUS=$?
    
    if [ $MAP_STATUS -eq 0 ]; then
        echo -e "${GREEN}Map generation completed successfully!${NC}"
    else
        handle_error "Map generation failed. Check the logs for details."
    fi
else
    handle_error "Environment verification failed"
fi

# Keep terminal open on success too
echo "Press Enter to exit..."
read
