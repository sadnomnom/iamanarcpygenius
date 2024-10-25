#!/bin/bash

# First verify pytest is working
echo "Verifying pytest installation..."
python -m scripts.cli verify

# Run unit tests with plain assertions to avoid arcpy conflicts
echo -e "\nRunning unit tests..."
python -m pytest --assert=plain -m unit tests/unit/

# If unit tests pass, run integration tests
echo -e "\nRunning integration tests..."
python -m pytest --assert=plain -m integration tests/integration/

# Finally, show test coverage (only if previous tests pass)
echo -e "\nRunning all tests with coverage..."
python -m pytest --assert=plain --cov=scripts tests/
