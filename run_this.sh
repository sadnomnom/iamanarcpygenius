#!/bin/bash

# Step 1: Verify environment setup
echo "Verifying environment setup..."
python -m scripts.cli verify

# Step 2: Process intersections (create base files)
echo "Processing intersections..."
python -m scripts.cli process-intersections

# Step 3: Process vegetation management
echo "Processing vegetation management..."
python -m scripts.cli process-veg

# Step 4: Generate maps and PDFs
echo "Generating maps and PDFs..."
python -m scripts.cli process-maps
