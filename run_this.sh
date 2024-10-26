#!/bin/bash

# Disable terminal logger traps temporarily
trap - DEBUG

# Set environment variables
export PYTHONPATH="."
export ARCGIS_PYTHON_API_VERSION=3.0
export PYTHONUNBUFFERED=1  # Force unbuffered output
export PYTHONIOENCODING=utf-8  # Ensure proper encoding

# Default test values
TEST_SUBSTATION="EMILIE"
TEST_YEAR="2024"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Simple error handler
handle_error() {
    echo -e "${RED}$1${NC}"
    exit 1
}

# Run verification
echo "Verifying environment setup..."
python -u -m scripts.cli verify
VERIFY_STATUS=$?

if [ $VERIFY_STATUS -eq 0 ]; then
    echo -e "${GREEN}Verification successful!${NC}"
    
    # Run map generation
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
