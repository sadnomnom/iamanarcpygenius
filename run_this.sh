#!/bin/bash

# First, run unit tests to verify our mocking setup
echo "Running unit tests..."
python -m scripts.cli test -t unit

# If unit tests pass, run integration tests
echo -e "\nRunning integration tests..."
python -m scripts.cli test -t integration

# Finally, show test coverage
echo -e "\nRunning all tests with coverage..."
python -m pytest --cov=scripts tests/
