#!/bin/bash

# Function to check last command status
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

# Step 1: Verify environment setup
echo "Verifying environment setup..."
python -m scripts.cli verify
check_status "Environment verification"

# Ask user for processing mode
echo -e "\nSelect processing mode:"
echo "1. GUI Mode"
echo "2. Command Line Mode"
read -p "Enter choice (1 or 2): " mode

if [ "$mode" = "1" ]; then
    # Launch GUI
    echo "Launching GUI..."
    python -m scripts.cli gui
    
else
    # Command Line Mode
    # Get processing parameters
    read -p "Enter source substation: " source_sub
    read -p "Enter processing year [2024]: " year
    year=${year:-2024}
    
    # Step 2: Generate maps
    echo -e "\nGenerating maps..."
    python -m scripts.cli generate-maps "$source_sub" --year "$year"
    check_status "Map generation"
    
    echo -e "\nProcessing complete!"
fi
