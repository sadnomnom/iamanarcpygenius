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
VERIFY_STATUS=$?

if [ $VERIFY_STATUS -eq 0 ]; then
    echo -e "${GREEN}Verification successful!${NC}"
    
    # Run the main script with command line arguments
    python -m scripts.cli generate-maps "$TEST_SUBSTATION" --year "$TEST_YEAR"
    MAP_STATUS=$?
    
    if [ $MAP_STATUS -eq 0 ]; then
        echo -e "${GREEN}Map generation completed successfully!${NC}"
    else
        echo -e "${RED}Map generation failed. Check the logs for details.${NC}"
        echo "Press any key to continue..."
        read -n 1
        exit $MAP_STATUS
    fi
else
    echo -e "${RED}Environment verification failed${NC}"
    echo "Press any key to continue..."
    read -n 1
    exit $VERIFY_STATUS
fi

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo "Press any key to continue..."
    read -n 1
fi
