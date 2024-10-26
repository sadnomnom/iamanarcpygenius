#!/bin/bash

# Set environment variables
export PYTHONPATH="."
export ARCGIS_PYTHON_API_VERSION=3.0

# Default test values for debugging
TEST_SUBSTATION="EMILIE"  # Valid substation from config
TEST_YEAR="2024"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Verifying environment setup..."

# Run verification first
python -m scripts.cli verify

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Verification successful!${NC}"
    
    # Run the main script with command line arguments instead of echo
    python -m scripts.cli generate-maps "$TEST_SUBSTATION" --year "$TEST_YEAR"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Map generation completed successfully!${NC}"
    else
        echo -e "${RED}Map generation failed. Check the logs for details.${NC}"
        exit 1
    fi
else
    echo -e "${RED}Environment verification failed${NC}"
    exit 1
fi
