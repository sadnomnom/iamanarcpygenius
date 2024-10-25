#!/bin/bash

# Create base directories
directories=(
    "config"
    "data/input/mxd"
    "data/input/aprx"
    "data/output/pdf"
    "data/output/logs"
    "scripts/helpers"
    "tests"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
done

# Set environment variables to disable SSL verification
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PYTHONHTTPSVERIFY=0

# Create Python virtual environment and activate it
python -m venv venv
source venv/bin/activate

# Upgrade pip and install requirements with SSL verification disabled
echo -e "\nUpgrading pip and installing requirements...\n"
python -m pip install --upgrade pip --no-warn-script-location --disable-pip-version-check --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Install each package individually with SSL verification disabled
packages=(
    "click>=8.0.0"
    "pandas>=1.3.0"
    "PyYAML>=5.4.1"
    "pytest>=7.0.0"
    "pytest-cov>=4.0.0"
)

for package in "${packages[@]}"; do
    echo "Installing $package..."
    python -m pip install --no-deps --no-cache-dir --disable-pip-version-check --trusted-host pypi.org --trusted-host files.pythonhosted.org "$package"
done

# Create .gitkeep files
echo -e "\nCreating .gitkeep files...\n"
touch "data/input/mxd/.gitkeep"
touch "data/input/aprx/.gitkeep"
touch "data/output/pdf/.gitkeep"
touch "data/output/logs/.gitkeep"

# Verify pytest installation
echo -e "\nVerifying pytest installation...\n"
python -m pip list | grep "pytest"

# Verify the structure was created
echo -e "\nProject structure created successfully!\n"
find . -type d

echo -e "\nEnvironment setup complete!\n"
echo "Note: Make sure you have ArcGIS installed for arcpy functionality"
echo "To activate the environment in the future, run: source venv/bin/activate"
